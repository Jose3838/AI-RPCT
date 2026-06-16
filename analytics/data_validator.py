from pathlib import Path
import pandas as pd

required_files = [
    "data/market_data.csv",
    "data/gpu_data.csv",
    "data/rpct_scores.csv",
    "data/provider_rankings.csv",
    "data/shortage_probability.csv",
    "data/forecast_signal.csv",
    "data/trend_signal.csv"
]

errors = []

for file in required_files:
    path = Path(file)

    if not path.exists():
        errors.append(f"Missing file: {file}")
        continue

    if file.endswith(".csv"):
        df = pd.read_csv(path)
        if df.empty:
            errors.append(f"Empty file: {file}")

if errors:
    print("DATA VALIDATION FAILED")
    for error in errors:
        print("-", error)
    raise SystemExit(1)

print("DATA VALIDATION PASSED")
