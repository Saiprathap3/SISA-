import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    anthropic_api_key: str = ""
    claude_model: str = "claude-sonnet-4-6"
    frontend_origin: str = "http://localhost:5173"
    allowed_origins: str = "http://localhost:3000,http://localhost:5173"
    api_bearer_token: str = "sisa-hackathon-secure-2025"
    max_file_size_mb: int = 10
    app_version: str = "1.0.0"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()


def get_cors_origins() -> list:
    """
    Returns CORS origins based on environment.
    In production: uses FRONTEND_URL env variable.
    In development: uses localhost.
    """
    env = os.getenv("ENVIRONMENT", "development")

    if env == "production":
        frontend_url = os.getenv("FRONTEND_URL", "")
        origins = [
            frontend_url,
            "https://*.vercel.app",  # Vercel preview deployments
        ]
        return [o for o in origins if o]  # remove empty strings

    return [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]


if not settings.anthropic_api_key:
    print("WARNING: ANTHROPIC_API_KEY not set - AI insights will use fallback")
else:
    print(f"API Key loaded: {settings.anthropic_api_key[:12]}...")
    print(f"Model: {settings.claude_model}")
    print(f"CORS: {get_cors_origins()}")
