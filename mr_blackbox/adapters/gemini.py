import json
import os
from pathlib import Path
from typing import Optional, List
from mr_blackbox.engine.models import Usage, Session

class GeminiAdapter:
    def __init__(self):
        # Gemini telemetry can be global or local
        self.global_settings_path = Path.home() / ".gemini" / "settings.json"

    def _get_telemetry_log(self, project_root: Path) -> Optional[Path]:
        """Finds the telemetry log for the project."""
        # 1. Check project-local .gemini/telemetry.log
        local_log = project_root / ".gemini" / "telemetry.log"
        if local_log.exists():
            return local_log
            
        # 2. In the future, parse settings.json for custom telemetry.outfile
        return None

    def ingest_session(self, session_id: str, project_root: Path) -> Optional[Usage]:
        """Parses Gemini telemetry/summary data."""
        # Note: Gemini CLI doesn't always use a clear 'session_id' in telemetry.log
        # unless specifically tagged. We'll use timestamps or specific summary files if available.
        
        # Check for specific session summary first
        summary_path = project_root / ".mr-blackbox" / "cache" / f"gemini-{session_id}.json"
        if summary_path.exists():
            with open(summary_path, "r") as f:
                data = json.load(f)
                return self._parse_summary(data, session_id)

        log_path = self._get_telemetry_log(project_root)
        if not log_path:
            return None

        # Logic to parse telemetry.log for a specific session/time-range
        # For MVP Phase 2, we'll implement a basic summary parser
        return None

    def _parse_summary(self, data: dict, session_id: str) -> Usage:
        """Parses a standard Gemini session summary JSON."""
        usage = Usage(session_id=session_id)
        # Assuming the structure from Gemini CLI --session-summary
        u = data.get("usage", {})
        usage.input_tokens = u.get("prompt_tokens", 0)
        usage.output_tokens = u.get("candidates_tokens", 0)
        # Gemini 1.5 caching stats
        usage.cache_read_tokens = u.get("cached_content_tokens", 0)
        usage.total_tokens = usage.input_tokens + usage.output_tokens + usage.cache_read_tokens
        return usage

    def get_latest_session_id(self, project_root: Path) -> Optional[str]:
        """Heuristic to find the latest session."""
        log_path = self._get_telemetry_log(project_root)
        if not log_path: return None
        # Return a timestamp-based ID or similar
        return f"gemini-{int(os.path.getmtime(log_path))}"
