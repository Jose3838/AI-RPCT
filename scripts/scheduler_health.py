import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))


REPO_DIR = Path(__file__).resolve().parents[1]
LOG_DIR = REPO_DIR / "logs"
OUT_LOG = LOG_DIR / "launchd.daily.out.log"
ERR_LOG = LOG_DIR / "launchd.daily.err.log"
PLIST_PATH = Path.home() / "Library" / "LaunchAgents" / "com.airpct.daily.plist"


def file_age_hours(path, now=None):
    path = Path(path)
    if not path.exists():
        return None
    now = now or datetime.now(timezone.utc)
    modified_at = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    return round((now - modified_at).total_seconds() / 3600, 2)


def tail_text(path, limit=4000):
    path = Path(path)
    if not path.exists() or path.stat().st_size == 0:
        return ""
    content = path.read_text(errors="replace")
    return content[-limit:]


def build_scheduler_health(now=None):
    now = now or datetime.now(timezone.utc)
    out_tail = tail_text(OUT_LOG)
    err_tail = tail_text(ERR_LOG)
    out_age = file_age_hours(OUT_LOG, now=now)
    err_age = file_age_hours(ERR_LOG, now=now)
    last_run_completed = "CORE INTELLIGENCE DONE" in out_tail
    has_recent_error = bool(err_tail.strip()) and (err_age is None or err_age <= 24)

    if not PLIST_PATH.exists():
        status = "not_installed"
        next_action = "Run ./scripts/install_macos_launch_agent.sh."
    elif has_recent_error:
        status = "error_log_present"
        next_action = "Inspect logs/launchd.daily.err.log and rerun ./scripts/run_core_intelligence.sh."
    elif out_age is None:
        status = "installed_no_run_log"
        next_action = "Wait for the next login/daily run or run ./scripts/run_core_intelligence.sh manually."
    elif out_age > 30:
        status = "stale"
        next_action = "Wake the Mac and verify launchd with ./scripts/macos_launch_agent_status.sh."
    elif last_run_completed:
        status = "healthy"
        next_action = "Maintain daily collection cadence."
    else:
        status = "unknown_completion"
        next_action = "Inspect logs/launchd.daily.out.log for the latest run."

    return {
        "product": "AI-RPCT",
        "report_type": "scheduler_health",
        "status": status,
        "launch_agent_label": "com.airpct.daily",
        "plist_path": str(PLIST_PATH),
        "plist_installed": PLIST_PATH.exists(),
        "schedule": "login_and_daily_08_15_local_time",
        "out_log": str(OUT_LOG),
        "err_log": str(ERR_LOG),
        "out_log_age_hours": out_age,
        "err_log_age_hours": err_age,
        "last_run_completed": last_run_completed,
        "has_recent_error": has_recent_error,
        "next_action": next_action,
    }


def main():
    print(json.dumps(build_scheduler_health(), indent=2, default=str))


if __name__ == "__main__":
    main()
