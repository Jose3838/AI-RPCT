import pandas as pd
from pathlib import Path

rows = []

def read_provider_csv(path):
    if not path.exists() or path.stat().st_size <= 1:
        return pd.DataFrame(columns=[
            "provider",
            "gpu",
            "price_per_hour",
            "availability",
            "timestamp"
        ])
    return pd.read_csv(path)

# Vast
if Path("data/live_provider_data.csv").exists():
    vast = read_provider_csv(Path("data/live_provider_data.csv"))

    rows.append({
        "provider": "vast",
        "offers": len(vast),
        "gpu_types": vast["gpu"].nunique(),
        "avg_price": round(vast["price_per_hour"].mean(), 4)
    })

# RunPod
if Path("data/runpod_live_report.csv").exists():
    runpod = read_provider_csv(Path("data/runpod_live_report.csv"))

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
