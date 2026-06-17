import time
from datetime import datetime

from automated_intelligence_snapshot_v2 import run_intelligence_snapshot_v2


def run_hourly_loop():
    while True:
        print("Running snapshot at", datetime.utcnow().isoformat())
        result = run_intelligence_snapshot_v2()
        print(result)
        print("Sleeping for 1 hour...")
        time.sleep(3600)


if __name__ == "__main__":
    run_hourly_loop()
