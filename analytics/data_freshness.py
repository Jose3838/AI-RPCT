from pathlib import Path
from datetime import datetime
import pandas as pd

files = [
    "data/gpu_data.csv",
    "data/market_data.csv",
    "data/rpct_scores.csv",
    "data/provider_rankings.csv",
    "data/ai_infrastructure_index.csv"
]

rows = []

for file in files:
    path = Path(file)
    if path.exists():
        modified = datetime.fromtimestamp(path.stat().st_mtime)
        age_hours = round((datetime.now() - modified).total_seconds() / 3600, 2)
        rows.append({
            "file": file,
            "exists": True,
            "age_hours": age_hours,
            "fresh": age_hours <= 24
        })
    else:
        rows.append({
            "file": file,
            "exists": False,
            "age_hours": None,
            "fresh": False
        })

df = pd.DataFrame(rows)
df.to_csv("data/data_freshness.csv", index=False)

print(df)
