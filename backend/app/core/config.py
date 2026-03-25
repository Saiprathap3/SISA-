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
        extra="ignore"   # NEVER "forbid"
    )

settings = Settings()

allowed_origins_list = [
    o.strip() for o in settings.allowed_origins.split(",")
]

# Startup validation
if not settings.anthropic_api_key:
    print("WARNING: ANTHROPIC_API_KEY not set — AI insights will use fallback")
else:
    print(f"✅ API Key loaded: {settings.anthropic_api_key[:12]}...")
    print(f"✅ Model: {settings.claude_model}")
    print(f"✅ CORS: {allowed_origins_list}")
