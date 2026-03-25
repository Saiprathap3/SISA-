from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings, allowed_origins_list
from app.api.routes.analyze import router as analyze_router

app = FastAPI(
    title="AI Secure Data Intelligence Platform",
    description="AI Gateway + Scanner + Log Analyzer + Risk Engine",
    version=settings.app_version
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze_router, tags=["Analysis"])

@app.get("/")
async def root():
    return {
        "name": "AI Secure Data Intelligence Platform",
        "version": settings.app_version,
        "model": settings.claude_model,
        "endpoints": ["/analyze", "/health", "/patterns", "/docs"]
    }
