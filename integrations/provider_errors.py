import pandas as pd
from pathlib import Path
from datetime import datetime

ERROR_FILE = "data/provider_errors.csv"

def log_provider_error(provider, error):
    row = pd.DataFrame([{
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "provider": provider,
        "error": str(error)
    }])

    if Path(ERROR_FILE).exists():
        old = pd.read_csv(ERROR_FILE)
        out = pd.concat([old, row], ignore_index=True)
    else:
        out = row

    out.to_csv(ERROR_FILE, index=False)
