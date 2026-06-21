from datetime import datetime, timezone
from pathlib import Path
import json
import traceback

from main import run_master_daily_cycle_v2

from intelligence.master_intelligence_collector import (
    run_master_intelligence_collector
)


LOG_FILE = Path("logs/master_daily_cycle.log")
JSON_FILE = Path("data/master_daily_cycle_latest.json")

def run():
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    JSON_FILE.parent.mkdir(parents=True, exist_ok=True)

    started_at = datetime.now(timezone.utc).isoformat()

    try:
        result = run_master_daily_cycle_v2()
        intelligence_collection = run_master_intelligence_collector()

        payload = {
            "status": "success",
            "started_at": started_at,
            "finished_at": datetime.now(timezone.utc).isoformat(),
            "result": result,
            "intelligence_collection": intelligence_collection,
        }

        JSON_FILE.write_text(json.dumps(payload, indent=2, default=str))

        with LOG_FILE.open("a") as f:
            f.write(f"{payload['finished_at']} SUCCESS master_daily_cycle_v2\n")

        print(json.dumps(payload, indent=2, default=str))

    except Exception as error:
        payload = {
            "status": "error",
            "started_at": started_at,
            "finished_at": datetime.now(timezone.utc).isoformat(),
            "error": str(error),
            "traceback": traceback.format_exc(),
        }

        JSON_FILE.write_text(json.dumps(payload, indent=2, default=str))

        with LOG_FILE.open("a") as f:
            f.write(f"{payload['finished_at']} ERROR {error}\n")

        print(json.dumps(payload, indent=2, default=str))
        raise

if __name__ == "__main__":
    run()
