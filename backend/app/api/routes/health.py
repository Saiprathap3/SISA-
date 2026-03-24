import time
from fastapi import APIRouter
from app.core.config import settings

start_time = time.time()
router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok", "version": settings.APP_VERSION, "uptime_seconds": time.time() - start_time}
from fastapi import APIRouter
import time
from app.core.config import settings

router = APIRouter()
start_time = time.time()


@router.get('/health')
async def health():
    uptime = time.time() - start_time
    return {"status": "ok", "version": settings.APP_VERSION, "uptime_seconds": uptime}
