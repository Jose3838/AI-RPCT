import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from apscheduler.schedulers.background import BackgroundScheduler

from automated_intelligence_snapshot_v2 import run_intelligence_snapshot_v2
from utils.logger import log

STATUS_FILE = Path("data/scheduler_status.json")
MAX_HISTORY = 20
CONSECUTIVE_FAILURE_ALERT_THRESHOLD = 3
RETRY_DELAY_SECONDS = 5

_scheduler = None


def _send_alert(message):
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    if not webhook_url:
        return

    try:
        requests.post(webhook_url, json={"text": message}, timeout=10)
    except Exception as exc:
        log(f"scheduler: alert delivery failed: {exc}")


def _run_step_with_retry(name, func):
    try:
        func()
        return "ok"
    except Exception as first_exc:
        log(f"scheduler: {name} failed ({first_exc}), retrying once")
        time.sleep(RETRY_DELAY_SECONDS)

        try:
            func()
            return "ok (recovered on retry)"
        except Exception as second_exc:
            log(f"scheduler: {name} failed again after retry: {second_exc}")
            return f"error: {second_exc}"


def _run_history_snapshot():
    result = subprocess.run(
        [sys.executable, "jobs/history_snapshot.py"],
        capture_output=True,
        text=True,
        timeout=120
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr[:300] or "non-zero exit")


def _load_status_file():
    if not STATUS_FILE.exists():
        return {"history": [], "consecutive_failures": 0}

    return json.loads(STATUS_FILE.read_text())


def run_daily_pipeline():
    started_at = datetime.now(timezone.utc).isoformat()
    log(f"scheduler: daily pipeline started at {started_at}")

    steps = {
        "intelligence_snapshot_v2": _run_step_with_retry(
            "intelligence_snapshot_v2", run_intelligence_snapshot_v2
        ),
        "history_snapshot": _run_step_with_retry(
            "history_snapshot", _run_history_snapshot
        ),
    }

    finished_at = datetime.now(timezone.utc).isoformat()
    overall_status = (
        "ok" if all(v.startswith("ok") for v in steps.values()) else "degraded"
    )

    state = _load_status_file()
    consecutive_failures = (
        0 if overall_status == "ok"
        else state.get("consecutive_failures", 0) + 1
    )

    run_record = {
        "status": overall_status,
        "started_at": started_at,
        "finished_at": finished_at,
        "steps": steps
    }

    history = state.get("history", [])
    history.append(run_record)
    history = history[-MAX_HISTORY:]

    _write_status({
        **run_record,
        "history": history,
        "consecutive_failures": consecutive_failures
    })

    log(f"scheduler: daily pipeline finished at {finished_at} ({overall_status})")

    if consecutive_failures >= CONSECUTIVE_FAILURE_ALERT_THRESHOLD:
        alert_message = (
            f"AI-RPCT daily pipeline has failed {consecutive_failures} times "
            f"in a row. Latest steps: {steps}"
        )
        log(f"scheduler: {alert_message}")
        _send_alert(alert_message)

    return run_record


def _write_status(status):
    STATUS_FILE.parent.mkdir(exist_ok=True)
    STATUS_FILE.write_text(json.dumps(status, indent=2))


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
