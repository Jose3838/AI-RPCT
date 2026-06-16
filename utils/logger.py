from datetime import datetime
from pathlib import Path

LOG_FILE = "data/system.log"

def log(message):
    Path("data").mkdir(exist_ok=True)

    with open(LOG_FILE, "a") as f:
        f.write(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {message}\n"
        )
