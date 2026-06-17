import pandas as pd
from pathlib import Path

ACCESS_FILE = "data/plan_access_matrix.csv"

def has_access(plan, endpoint):
    if not plan:
        return False

    if not Path(ACCESS_FILE).exists():
        return False

    df = pd.read_csv(ACCESS_FILE)

    row = df[df["endpoint"] == endpoint]

    if row.empty:
        return False

    if plan not in row.columns:
        return False

    value = row.iloc[0][plan]

    return str(value).lower() == "true"
