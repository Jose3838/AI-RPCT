import pandas as pd
from pathlib import Path
from datetime import datetime

USAGE_FILE = "data/api_usage.csv"

def log_usage(api_key, endpoint):
    row = pd.DataFrame([{
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "api_key": api_key,
        "endpoint": endpoint
    }])

    if Path(USAGE_FILE).exists():
        old = pd.read_csv(USAGE_FILE)
        out = pd.concat([old, row], ignore_index=True)
    else:
        out = row

    out.to_csv(USAGE_FILE, index=False)
