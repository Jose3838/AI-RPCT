from pathlib import Path
import pandas as pd

files = [
    "data/market_data.csv",
    "data/gpu_data.csv",
    "data/rpct_scores.csv",
    "data/provider_rankings.csv",
    "data/shortage_probability.csv",
    "data/forecast_signal.csv",
    "data/trend_signal.csv",
    "data/api_metrics.json",
    "dashboard.html"
]

print("\nAI-RPCT SYSTEM STATUS")
print("=====================\n")

for file in files:
    path = Path(file)
    if path.exists():
        if file.endswith(".csv"):
            rows = len(pd.read_csv(path))
            print(f"OK  {file} | rows={rows}")
        else:
            print(f"OK  {file}")
    else:
        print(f"MISS {file}")

print("\nStatus check complete.")
