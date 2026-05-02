import json
import os
from pathlib import Path
from typing import Optional, List
from mr_blackbox.engine.models import Usage

class CodexAdapter:
    def __init__(self):
        # Codex experimental support
        self.history_path = Path.home() / ".codex" / "history"

    def ingest_session(self, session_id: str, project_root: Path) -> Optional[Usage]:
        """Parses Codex history or quota data."""
        # Since Codex CLI data is sparse, we might rely on history entry counts
        # or a specific 'status' output file if provided by the user.
        
        status_file = project_root / ".mr-blackbox" / "cache" / f"codex-{session_id}.json"
        if status_file.exists():
            with open(status_file, "r") as f:
                data = json.load(f)
                return self._parse_status(data, session_id)
        
        # Fallback: estimate based on generic session info
        return Usage(session_id=session_id, total_tokens=0) # Will mark as estimated

    def _parse_status(self, data: dict, session_id: str) -> Usage:
        """Parses a Codex status/quota JSON."""
        usage = Usage(session_id=session_id)
        # Assuming Codex might expose 'requests_made' or 'quota_used'
        # We'll map these to a derived token count for the engine
        reqs = data.get("requests_made", 0)
        usage.input_tokens = reqs * 1000 # Rough estimation: 1k per request
        usage.output_tokens = reqs * 500  # Rough estimation: 500 per request
        usage.total_tokens = usage.input_tokens + usage.output_tokens
        return usage

    def get_latest_session_id(self, project_root: Path) -> Optional[str]:
        # Return a generic ID if no better source exists
        return f"codex-{int(os.path.getmtime(project_root))}"
