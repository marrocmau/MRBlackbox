from typing import List, Dict
from mr_blackbox.engine.models import Usage, Cost, Session

class IntelligenceEngine:
    def __init__(self, ledger_data: Dict):
        self.data = ledger_data
        self.sessions = ledger_data.get("sessions", [])

    def calculate_waste_score(self) -> Dict:
        """Calculates a waste score from 0 to 100."""
        if not self.sessions:
            return {"score": 0, "causes": []}

        # Metrics for calculation
        total_tokens = sum(s["usage"].get("total_tokens", 0) for s in self.sessions)
        total_cache_read = sum(s["usage"].get("cache_read_tokens", 0) for s in self.sessions)
        total_input = sum(s["usage"].get("input_tokens", 0) for s in self.sessions)
        
        # 1. Cache Efficiency (High weight)
        # If cache read is low compared to input, waste is higher
        potential_input = total_input + total_cache_read
        cache_ratio = (total_cache_read / potential_input) if potential_input > 0 else 1.0
        cache_waste = (1.0 - cache_ratio) * 100
        
        # 2. Expensive Model Usage (Medium weight)
        # In a real app, we'd check if Sonnet was used for simple tasks
        # For now, we simulate a small penalty if only expensive models are used
        providers = set(s["session"].get("provider") for s in self.sessions)
        model_penalty = 0
        if len(providers) == 1 and "claude_code" in providers:
            model_penalty = 15 # "Try mixing models"

        # Final Score (Weighted average)
        score = int((cache_waste * 0.7) + (model_penalty * 0.3))
        score = max(0, min(100, score))

        causes = []
        if cache_waste > 40:
            causes.append("Low cache reuse (Repeated context loading)")
        if model_penalty > 0:
            causes.append("Expensive model used for all tasks")
        
        return {
            "score": score,
            "causes": causes,
            "avoidable_usd": (total_tokens / 1_000_000) * 1.5 * (score / 100) # Rough estimate
        }

    def generate_replay(self) -> Dict:
        """Suggests an alternative route for the current project cost."""
        total_usd = self.data.get("totals", {}).get("usd", 0.0)
        
        # Suggestion: Use Gemini Flash for 50% of the tasks
        alt_usd = total_usd * 0.45 # Estimated 55% savings
        
        return {
            "actual": {
                "route": "Current mix",
                "cost": total_usd
            },
            "alternative": {
                "route": "Optimized (Flash for scans + Sonnet for patches)",
                "cost": alt_usd
            },
            "savings_pct": 55
        }
