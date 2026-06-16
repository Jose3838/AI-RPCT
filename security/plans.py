import pandas as pd
from pathlib import Path

API_KEYS_FILE = "data/api_keys.csv"

def get_plan_for_key(api_key):
    if not Path(API_KEYS_FILE).exists():
        return None

    df = pd.read_csv(API_KEYS_FILE)

    match = df[df["key"] == api_key]

    if match.empty:
        return None

    return match.iloc[0]["plan"]
