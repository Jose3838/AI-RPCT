import pandas as pd
from pathlib import Path

KEY_FILE = "data/api_key_registry.csv"

def resolve_plan(api_key):
    if not api_key:
        return None

    if not Path(KEY_FILE).exists():
        return None

    df = pd.read_csv(KEY_FILE)

    match = df[
        (df["key"] == api_key) &
        (df["status"] == "active")
    ]

    if match.empty:
        return None

    return match.iloc[0]["plan"]
