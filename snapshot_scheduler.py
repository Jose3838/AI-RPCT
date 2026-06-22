import json
from datetime import datetime, timezone

from api.terminal_core import save_market_pulse_snapshot
from automated_snapshot_runner import run_daily_snapshot


def run_scheduled_snapshot(
    snapshot_runner=run_daily_snapshot,
    pulse_recorder=save_market_pulse_snapshot,
):
    result = snapshot_runner()
    pulse_snapshot = pulse_recorder()

    return {
        "status": "ok",
        "executed_at": datetime.now(timezone.utc).isoformat(),
        "snapshot_result": result,
        "market_pulse_snapshot": pulse_snapshot,
    }


if __name__ == "__main__":
    print(json.dumps(run_scheduled_snapshot(), indent=2))
