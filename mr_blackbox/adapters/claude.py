import json
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, List
from mr_blackbox.engine.models import Usage, Session

class ClaudeAdapter:
    def __init__(self):
        self.base_path = Path.home() / ".claude" / "projects"

    def _get_project_dir(self, project_root: Path) -> Optional[Path]:
        """Finds the Claude project directory based on the local project root."""
        # Claude often uses the absolute path with dashes instead of slashes
        # or similar naming conventions.
        # For now, we'll list the directories and check metadata if available.
        if not self.base_path.exists():
            return None
        
        # Try exact match or fuzzy match
        project_name_slug = str(project_root.absolute()).replace("/", "-").lstrip("-")
        potential_dir = self.base_path / project_name_slug
        if potential_dir.exists():
            return potential_dir
            
        # Fallback: look into sessions-index.json of each dir if it exists
        # This is more expensive but accurate.
        return None

    def ingest_session(self, session_id: str, project_root: Path) -> Optional[Usage]:
        """Parses a Claude session transcript and returns Usage data."""
        project_dir = self._get_project_dir(project_root)
        if not project_dir:
            return None
            
        transcript_path = project_dir / f"{session_id}.jsonl"
        if not transcript_path.exists():
            return None
            
        usage = Usage(session_id=session_id)
        
        with open(transcript_path, "r") as f:
            for line in f:
                if not line.strip(): continue
                try:
                    event = json.loads(line)
                    # Claude transcripts contain usage events or summaries
                    # We look for keys like 'usage', 'token_usage', etc.
                    # Note: The exact structure might vary, this is an assumption based on common AI tool patterns.
                    if "usage" in event:
                        u = event["usage"]
                        usage.input_tokens += u.get("input_tokens", 0)
                        usage.output_tokens += u.get("output_tokens", 0)
                        usage.cache_read_tokens += u.get("cache_read_tokens", 0)
                        usage.cache_write_tokens += u.get("cache_write_tokens", 0)
                except Exception:
                    continue
                    
        usage.total_tokens = usage.input_tokens + usage.output_tokens + usage.cache_read_tokens + usage.cache_write_tokens
        return usage

    def get_latest_session_id(self, project_root: Path) -> Optional[str]:
        """Finds the latest session ID for a project."""
        project_dir = self._get_project_dir(project_root)
        if not project_dir:
            return None
            
        index_path = project_dir / "sessions-index.json"
        if index_path.exists():
            with open(index_path, "r") as f:
                index = json.load(f)
                # Assuming index is a list or has a 'sessions' key
                sessions = index.get("sessions", []) if isinstance(index, dict) else index
                if sessions:
                    # Return the ID of the latest session
                    return sessions[-1].get("id")
        return None
