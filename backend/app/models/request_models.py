from typing import Literal, Optional
from pydantic import BaseModel, Field


InputType = Literal["text", "file", "sql", "log", "chat"]


class AnalyzeOptions(BaseModel):
    mask: bool = Field(True, description="Mask sensitive values in output")
    log_analysis: bool = Field(True, description="Whether to call AI analysis")
    block_high_risk: bool = Field(True, description="Block when critical findings are present")


class AnalyzeRequest(BaseModel):
    input_type: InputType = Field(...)
    content: Optional[str] = Field(None)
    filename: Optional[str] = Field(None)
    options: AnalyzeOptions = Field(default_factory=AnalyzeOptions)

