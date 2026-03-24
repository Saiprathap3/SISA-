from typing import List, Optional
from pydantic import Field, validator
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    # Core
    ANTHROPIC_API_KEY: Optional[str] = None
    CLAUDE_MODEL: str = "claude-sonnet-4-6"
    APP_VERSION: str = "1.1.0"
    
    # Security
    API_BEARER_TOKEN: Optional[str] = None
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:5173"
    RATE_LIMIT: str = "30/minute"
    MAX_FILE_SIZE_MB: int = 10
    MAX_TEXT_CHARS: int = 50000

    # Detection
    ENABLE_ML: bool = True
    MIN_ML_SAMPLES: int = 50

    class Config:
        env_file = str(Path(__file__).resolve().parents[2] / ".env")
        env_file_encoding = "utf-8"

    @validator("ANTHROPIC_API_KEY")
    def validate_api_key(cls, v):
        if not v or v.strip() == "":
            raise ValueError("ANTHROPIC_API_KEY is missing or empty")
        return v

    @validator("CLAUDE_MODEL")
    def validate_model(cls, v):
        if not v or v.strip() == "":
            raise ValueError("CLAUDE_MODEL is not a valid string")
        return v


settings = Settings()


def allowed_origins_list() -> List[str]:
    return [o.strip() for o in settings.ALLOWED_ORIGINS.split(',')]
