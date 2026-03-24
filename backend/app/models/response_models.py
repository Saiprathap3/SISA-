from typing import List, Literal, Optional
from pydantic import BaseModel, Field


RiskLevel = Literal["low", "medium", "high", "critical"]
ActionTaken = Literal["allowed", "masked", "blocked"]


class Finding(BaseModel):
    type: str
    risk: RiskLevel
    line: Optional[int] = None
    masked_value: str
    original_line: Optional[str] = None


class AnalyzeResponse(BaseModel):
    summary: str
    content_type: str
    findings: List[Finding]
    risk_score: int
    risk_level: RiskLevel
    action: ActionTaken
    insights: List[str] = Field(default_factory=list)
    anomalies: List[str] = Field(default_factory=list)
    ai_used: bool = False
    request_id: str
    duration_ms: float

