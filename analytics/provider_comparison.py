import pandas as pd
from pathlib import Path

rows = []

# Vast
if Path("data/live_provider_data.csv").exists():
    vast = pd.read_csv("data/live_provider_data.csv")

    rows.append({
        "provider": "vast",
        "offers": len(vast),
        "gpu_types": vast["gpu"].nunique(),
        "avg_price": round(vast["price_per_hour"].mean(), 4)
    })

# RunPod
if Path("data/runpod_live_report.csv").exists():
    runpod = pd.read_csv("data/runpod_live_report.csv")

    rows.append({
        "provider": "runpod",
        "offers": len(runpod),
        "gpu_types": runpod["gpu"].nunique(),
        "avg_price": round(runpod["price_per_hour"].mean(), 4)
    })

df = pd.DataFrame(rows)

df.to_csv(
    "data/provider_comparison.csv",
    index=False
)

print(df)
