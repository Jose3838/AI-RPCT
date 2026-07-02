import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from apscheduler.schedulers.background import BackgroundScheduler

from automated_intelligence_snapshot_v2 import run_intelligence_snapshot_v2
from utils.logger import log

STATUS_FILE = Path("data/scheduler_status.json")

_scheduler = None


def _write_status(status):
    STATUS_FILE.parent.mkdir(exist_ok=True)
    STATUS_FILE.write_text(json.dumps(status, indent=2))


def run_daily_pipeline():
    started_at = datetime.now(timezone.utc).isoformat()
    log(f"scheduler: daily pipeline started at {started_at}")

    steps = {}

    try:
        run_intelligence_snapshot_v2()
        steps["intelligence_snapshot_v2"] = "ok"
    except Exception as exc:
        steps["intelligence_snapshot_v2"] = f"error: {exc}"
        log(f"scheduler: intelligence_snapshot_v2 failed: {exc}")

    try:
        result = subprocess.run(
            [sys.executable, "jobs/history_snapshot.py"],
            capture_output=True,
            text=True,
            timeout=120
        )
        steps["history_snapshot"] = (
            "ok" if result.returncode == 0
            else f"error: {result.stderr[:300]}"
        )
    except Exception as exc:
        steps["history_snapshot"] = f"error: {exc}"
        log(f"scheduler: history_snapshot failed: {exc}")

    finished_at = datetime.now(timezone.utc).isoformat()
    overall_status = (
        "ok" if all(v == "ok" for v in steps.values()) else "degraded"
    )

    _write_status({
        "status": overall_status,
        "started_at": started_at,
        "finished_at": finished_at,
        "steps": steps
    })

    log(f"scheduler: daily pipeline finished at {finished_at} ({overall_status})")

    return {
        "status": overall_status,
        "started_at": started_at,
        "finished_at": finished_at,
        "steps": steps
    }


def get_scheduler_status():
    if not STATUS_FILE.exists():
        return {
            "status": "never_run",
            "scheduler_running": _scheduler is not None and _scheduler.running
        }

    status = json.loads(STATUS_FILE.read_text())
    status["scheduler_running"] = _scheduler is not None and _scheduler.running
    return status


def start_scheduler():
    global _scheduler

    if _scheduler is not None:
        return _scheduler

    _scheduler = BackgroundScheduler(timezone="UTC")
    _scheduler.add_job(
        run_daily_pipeline,
        trigger="cron",
        hour=6,
        minute=0,
        id="daily_pipeline",
        replace_existing=True
    )
    _scheduler.start()
    log("scheduler: started, daily pipeline scheduled for 06:00 UTC")

    return _scheduler


def stop_scheduler():
    global _scheduler

    if _scheduler is not None:
        _scheduler.shutdown(wait=False)
        _scheduler = None
        log("scheduler: stopped")
