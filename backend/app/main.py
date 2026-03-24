import time
import uuid
import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.core.config import settings, allowed_origins_list
from app.api.routes import analyze, health
from app.utils.logger import get_logger

logger = get_logger(__name__)

# Rate Limiter
limiter = Limiter(key_func=get_remote_address, default_limits=[settings.RATE_LIMIT])

app = FastAPI(title="SecureAI Intelligence Platform")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

origins = allowed_origins_list()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def secure_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    start = time.time()
    
    try:
        response = await call_next(request)
        duration_ms = (time.time() - start) * 1000.0
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Response-Time"] = f"{duration_ms:.2f}ms"
        return response
    except Exception as e:
        error_id = str(uuid.uuid4())
        logger.exception(f"Unhandled error [{error_id}]", extra={"error_id": error_id})
        return JSONResponse(
            status_code=500,
            content={"detail": "A generic server error occurred", "error_id": error_id}
        )

app.include_router(health.router)
app.include_router(analyze.router, prefix="/api")

@app.on_event("startup")
def startup_event():
    # Print Section 5 Confirmation
    print("══════════════════════════════════════════════")
    print("   SECUREAI PLATFORM — STARTUP CONFIRMATION")
    print("══════════════════════════════════════════════")
    if settings.ANTHROPIC_API_KEY:
        print(" ✅ API Key loaded")
    print(f" ✅ Model: {settings.CLAUDE_MODEL}")
    print(f" ✅ CORS: {origins}")
    print(" ✅ Detection layers: Regex + Statistical + ML + AI")
    print("══════════════════════════════════════════════")
    logger.info(f"Server started v{settings.APP_VERSION}")
