from typing import Literal, Optional
from pydantic import BaseModel, Field


InputType = Literal["text", "file", "sql", "log", "chat"]


class AnalyzeOptions(BaseModel):
    mask_output: bool = Field(True, description="Mask sensitive values in output")
    use_ai: bool = Field(True, description="Whether to call AI analysis")
    block_on_critical: bool = Field(True, description="Block when critical findings are present")


class AnalyzeRequest(BaseModel):
    input_type: InputType = Field(...)
    content: Optional[str] = Field(None)
    filename: Optional[str] = Field(None)
    options: AnalyzeOptions = Field(default_factory=AnalyzeOptions)

