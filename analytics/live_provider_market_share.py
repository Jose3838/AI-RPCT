import pandas as pd
from pathlib import Path

rows = []

if Path("data/live_provider_data.csv").exists():
    vast = pd.read_csv("data/live_provider_data.csv")
    rows.append({
        "provider": "vast",
        "rows": len(vast)
    })

if Path("data/runpod_live_report.csv").exists():
    runpod = pd.read_csv("data/runpod_live_report.csv")
    rows.append({
        "provider": "runpod",
        "rows": len(runpod)
    })

df = pd.DataFrame(rows)

if not df.empty:
    total = df["rows"].sum()
    df["market_share_pct"] = round(df["rows"] / total * 100, 2)

df.to_csv("data/live_provider_market_share.csv", index=False)

print(df)
