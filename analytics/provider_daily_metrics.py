import pandas as pd
from datetime import datetime
from pathlib import Path

rankings = pd.read_csv(
    "data/provider_rankings.csv"
)

rankings["date"] = datetime.now().strftime("%Y-%m-%d")

history_file = "data/provider_daily_metrics.csv"

if Path(history_file).exists():
    old = pd.read_csv(history_file)
    rankings = pd.concat(
        [old, rankings],
        ignore_index=True
    )

rankings.to_csv(
    history_file,
    index=False
)

print(rankings.tail())
