import pandas as pd
from pathlib import Path

USERS_FILE = "users/users.csv"

def get_users():
    if not Path(USERS_FILE).exists():
        return []
    return pd.read_csv(USERS_FILE).to_dict(orient="records")
