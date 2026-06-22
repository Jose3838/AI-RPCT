import csv
import fcntl
from pathlib import Path
from datetime import datetime

USAGE_FILE = "data/api_usage.csv"


def log_usage(api_key, endpoint):
    path = Path(USAGE_FILE)
    path.parent.mkdir(parents=True, exist_ok=True)
    needs_header = not path.exists() or path.stat().st_size == 0

    with path.open("a", newline="") as file:
        fcntl.flock(file.fileno(), fcntl.LOCK_EX)
        writer = csv.DictWriter(file, fieldnames=["timestamp", "api_key", "endpoint"])

        if needs_header:
            writer.writeheader()

        writer.writerow({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "api_key": api_key,
            "endpoint": endpoint
        })

        file.flush()
        fcntl.flock(file.fileno(), fcntl.LOCK_UN)
