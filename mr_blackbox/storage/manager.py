import os
import json
from pathlib import Path
from typing import Optional

MR_DIR = ".mr-blackbox"

class StorageManager:
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.mr_path = base_path / MR_DIR

    def init_project(self, name: str, project_type: str = "other") -> bool:
        """Initializes the .mr-blackbox directory structure."""
        if self.mr_path.exists():
            return False
        
        # Create directories
        dirs = [
            "pricing",
            "sessions",
            "reports",
            "exports",
            "cache",
            "runtime"
        ]
        self.mr_path.mkdir(parents=True, exist_ok=True)
        for d in dirs:
            (self.mr_path / d).mkdir(exist_ok=True)
            
        # Create project.json
        from datetime import datetime
        project_config = {
            "project_id": name.lower().replace(" ", "-"),
            "name": name,
            "type": project_type,
            "created_at": datetime.now().isoformat(),
            "currency_primary": "USD",
            "currency_secondary": "EUR",
            "repo_path": str(self.base_path.absolute()),
        }
        
        with open(self.mr_path / "project.json", "w") as f:
            json.dump(project_config, f, indent=2)
            
        # Create empty ledger.json
        with open(self.mr_path / "ledger.json", "w") as f:
            json.dump({"sessions": [], "totals": {"usd": 0.0, "eur": 0.0, "tokens": 0}}, f, indent=2)
            
        return True

    def add_session_to_ledger(self, session: dict, usage: dict, cost: dict):
        """Adds a session and its associated data to the ledger."""
        ledger_path = self.mr_path / "ledger.json"
        
        # Helper to make dict JSON serializable
        def serialize(obj):
            if isinstance(obj, dict):
                return {k: serialize(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [serialize(i) for i in obj]
            elif hasattr(obj, "isoformat"):
                return obj.isoformat()
            return obj

        if not ledger_path.exists():
            data = {"sessions": [], "totals": {"usd": 0.0, "eur": 0.0, "tokens": 0}}
        else:
            with open(ledger_path, "r") as f:
                data = json.load(f)
        
        # Avoid duplicates
        if any(s["session"]["session_id"] == session["session_id"] for s in data["sessions"]):
            return False
            
        # Add session data
        combined_entry = serialize({
            "session": session,
            "usage": usage,
            "cost": cost
        })
        data["sessions"].append(combined_entry)
        
        # Update totals
        totals = data.get("totals", {})
        totals["usd"] = totals.get("usd", 0.0) + cost["total_usd"]
        totals["eur"] = totals.get("eur", 0.0) + cost["total_eur"]
        totals["tokens"] = totals.get("tokens", 0) + usage["total_tokens"]
        data["totals"] = totals
        
        with open(ledger_path, "w") as f:
            json.dump(data, f, indent=2)
            
        # Also save individual session file for backup/detail
        session_file = self.mr_path / "sessions" / f"{session['session_id']}.json"
        with open(session_file, "w") as f:
            json.dump(combined_entry, f, indent=2)
            
        return True

    @staticmethod
    def find_project_root(start_path: Path) -> Optional[Path]:
        """Traverses up to find the .mr-blackbox directory."""
        current = start_path.absolute()
        while current != current.parent:
            if (current / MR_DIR).exists():
                return current
            current = current.parent
        return None
