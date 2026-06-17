from pathlib import Path
import pandas as pd

files = [
    "data/gpu_price_history.csv",
    "data/provider_health_history.csv",
    "data/provider_market_share_history.csv"
]

rows = {}

for f in files:
    p = Path(f)

    if p.exists():
        rows[p.name] = len(pd.read_csv(p))
    else:
        rows[p.name] = 0

print(rows)
