from automated_snapshot_runner import run_daily_snapshot
from datetime import datetime


def run_scheduled_snapshot():
    result = run_daily_snapshot()

    return {
        "status": "ok",
        "executed_at": datetime.utcnow().isoformat(),
        "snapshot_result": result
    }


if __name__ == "__main__":
    print(
        run_scheduled_snapshot()
    )
