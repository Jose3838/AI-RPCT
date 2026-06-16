import pandas as pd
from pathlib import Path

files = [
    "data/provider_rankings.csv",
    "data/provider_marketshare.csv",
    "data/provider_concentration.csv",
    "data/provider_credentials.csv"
]

ok = 0

for file in files:
    if Path(file).exists() and not pd.read_csv(file).empty:
        ok += 1

score = round(ok / len(files) * 100, 2)

pd.DataFrame([{
    "provider_readiness_score": score
}]).to_csv("data/provider_readiness.csv", index=False)

print("Provider readiness:", score)
