import os
import time
import json
import sys
from pathlib import Path

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    HAS_WATCHDOG = True
except ImportError:
    HAS_WATCHDOG = False

# For the sake of this MVP, we'll assume the path is standard.
CLAUDE_HISTORY_PATH = Path.home() / ".claude" / "history.jsonl"

class ClaudeHistoryProcessor:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.last_position = self._get_file_size()

    def _get_file_size(self):
        if CLAUDE_HISTORY_PATH.exists():
            return CLAUDE_HISTORY_PATH.stat().st_size
        return 0

    def process_new_lines(self):
        new_size = self._get_file_size()
        if new_size <= self.last_position:
            self.last_position = new_size
            return

        with open(CLAUDE_HISTORY_PATH, "r") as f:
            f.seek(self.last_position)
            new_data = f.read()
            self.last_position = new_size
            
            for line in new_data.strip().split("\n"):
                if not line: continue
                try:
                    entry = json.loads(line)
                    if entry.get("working_directory") == str(self.project_root):
                        self._handle_new_session_event(entry)
                except Exception as e:
                    self._log(f"Error parsing line: {e}")

    def _handle_new_session_event(self, entry):
        session_id = entry.get('session_id')
        self._log(f"Detected event for session {session_id}")
        # In the future, this will call mr_blackbox.adapters.claude.ingest_session

    def _log(self, message):
        log_path = self.project_root / ".mr-blackbox" / "runtime" / "worker.log"
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(log_path, "a") as f:
            f.write(f"[{timestamp}] {message}\n")

if HAS_WATCHDOG:
    class ClaudeHistoryHandler(FileSystemEventHandler):
        def __init__(self, processor):
            self.processor = processor

        def on_modified(self, event):
            if Path(event.src_path) == CLAUDE_HISTORY_PATH:
                self.processor.process_new_lines()

def run_worker(project_root: Path):
    runtime_dir = project_root / ".mr-blackbox" / "runtime"
    pid_file = runtime_dir / "worker.pid"
    
    with open(pid_file, "w") as f:
        f.write(str(os.getpid()))
        
    processor = ClaudeHistoryProcessor(project_root)
    processor._log("Worker started")
    
    if HAS_WATCHDOG:
        processor._log("Using watchdog for file monitoring")
        observer = Observer()
        history_dir = CLAUDE_HISTORY_PATH.parent
        if not history_dir.exists(): history_dir.mkdir(parents=True, exist_ok=True)
        if not CLAUDE_HISTORY_PATH.exists(): CLAUDE_HISTORY_PATH.touch()
        
        handler = ClaudeHistoryHandler(processor)
        observer.schedule(handler, str(history_dir), recursive=False)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
    else:
        processor._log("Using polling for file monitoring (watchdog not found)")
        try:
            while True:
                processor.process_new_lines()
                time.sleep(2)
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <project_root>")
        sys.exit(1)
    run_worker(Path(sys.argv[1]))
