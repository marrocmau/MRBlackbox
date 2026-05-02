import json
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime
from mr_blackbox.engine.models import Usage, Cost

DEFAULT_PRICING = {
    "claude_code": {
        "claude-3-5-sonnet": {
            "input_per_1m": 3.00,
            "output_per_1m": 15.00,
            "cache_write_per_1m": 3.75,
            "cache_read_per_1m": 0.30
        },
        "claude-3-5-haiku": {
            "input_per_1m": 0.25,
            "output_per_1m": 1.25,
            "cache_write_per_1m": 0.30,
            "cache_read_per_1m": 0.03
        }
    },
    "gemini_cli": {
        "gemini-1.5-pro": {
            "input_per_1m": 3.50,
            "output_per_1m": 10.50,
            "cache_write_per_1m": 0.0,
            "cache_read_per_1m": 0.875
        },
        "gemini-1.5-flash": {
            "input_per_1m": 0.075,
            "output_per_1m": 0.30,
            "cache_write_per_1m": 0.0,
            "cache_read_per_1m": 0.01875
        }
    },
    "codex_cli": {
        "codex-base": {
            "input_per_1m": 2.00,
            "output_per_1m": 6.00,
            "cache_write_per_1m": 0.0,
            "cache_read_per_1m": 0.0
        }
    }
}

class CostEngine:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.pricing_path = project_root / ".mr-blackbox" / "pricing" / "current.json"
        self.forex_path = project_root / ".mr-blackbox" / "forex.json"
        self._ensure_default_pricing()

    def _ensure_default_pricing(self):
        if not self.pricing_path.exists():
            self.pricing_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.pricing_path, "w") as f:
                json.dump(DEFAULT_PRICING, f, indent=2)
        
        if not self.forex_path.exists():
            with open(self.forex_path, "w") as f:
                json.dump({"usd_to_eur": 0.94, "last_updated": datetime.now().isoformat()}, f, indent=2)

    def calculate_cost(self, usage: Usage, provider: str, model: str, mode: str = "exact") -> Cost:
        with open(self.pricing_path, "r") as f:
            pricing = json.load(f)
        
        rates = pricing.get(provider, {}).get(model)
        if not rates:
            # Fallback to default if not found in current snapshot
            rates = DEFAULT_PRICING.get(provider, {}).get(model, {})
            
        with open(self.forex_path, "r") as f:
            forex = json.load(f)
        
        forex_rate = forex.get("usd_to_eur", 0.94)
        
        input_cost = (usage.input_tokens / 1_000_000) * rates.get("input_per_1m", 0)
        output_cost = (usage.output_tokens / 1_000_000) * rates.get("output_per_1m", 0)
        cache_write_cost = (usage.cache_write_tokens / 1_000_000) * rates.get("cache_write_per_1m", 0)
        cache_read_cost = (usage.cache_read_tokens / 1_000_000) * rates.get("cache_read_per_1m", 0)
        
        total_usd = input_cost + output_cost + cache_write_cost + cache_read_cost
        total_eur = total_usd * forex_rate
        
        return Cost(
            session_id=usage.session_id,
            total_usd=total_usd,
            total_eur=total_eur,
            input_cost_usd=input_cost,
            output_cost_usd=output_cost,
            cached_input_cost_usd=cache_read_cost + cache_write_cost,
            forex_rate_usd_eur=forex_rate,
            calculation_mode=mode
        )
