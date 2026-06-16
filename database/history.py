import pandas as pd
from datetime import datetime
from pathlib import Path

def save_snapshot(df, name):
    Path("data").mkdir(exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y-%m-%d")
    path = f"data/history_{name}_{timestamp}.csv"
    df.to_csv(path, index=False)
    return path
