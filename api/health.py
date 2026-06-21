from fastapi import APIRouter
import time

router = APIRouter()

@router.get("/health")
def health():
    # attempt to read START_TIME from main to report uptime; fall back to 0
    try:
        from main import START_TIME
        uptime = int(time.time() - START_TIME)
    except Exception:
        uptime = 0

    return {
        "status": "ok",
        "uptime_seconds": uptime
    }


@router.get("/ready")
def ready():
    return {
        "status": "ok",
        "ready": True
    }
