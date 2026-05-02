from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Usage(BaseModel):
    session_id: str
    total_tokens: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    cached_input_tokens: int = 0
    cache_write_tokens: int = 0
    cache_read_tokens: int = 0
    reasoning_tokens: Optional[int] = 0
    tool_tokens: Optional[int] = 0
    thought_tokens: Optional[int] = 0

class Session(BaseModel):
    session_id: str
    project_id: str
    provider: str = "claude_code"
    started_at: datetime
    ended_at: Optional[datetime] = None
    duration_seconds: Optional[int] = 0
    cwd: str
    git_branch: Optional[str] = None
    task_label: Optional[str] = None
    feature_label: Optional[str] = None
    phase_label: Optional[str] = "development"
    calculation_mode: str = "exact" # exact, derived, estimated

class Cost(BaseModel):
    session_id: str
    total_usd: float = 0.0
    total_eur: float = 0.0
    input_cost_usd: float = 0.0
    output_cost_usd: float = 0.0
    cached_input_cost_usd: float = 0.0
    forex_rate_usd_eur: float = 0.0
    calculation_mode: str = "exact"
