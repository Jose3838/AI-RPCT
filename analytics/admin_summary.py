import pandas as pd
from pathlib import Path

summary = {}

files = {
    "rpct": "data/rpct_scores.csv",
    "providers": "data/provider_rankings.csv",
    "alerts": "data/alerts.csv",
    "data_quality": "data/data_quality.csv",
    "usage": "data/usage_metrics.csv"
}

for key, path in files.items():
    if Path(path).exists():
        summary[key] = len(pd.read_csv(path))
    else:
        summary[key] = 0

pd.DataFrame([summary]).to_csv("data/admin_summary.csv", index=False)

print(summary)
