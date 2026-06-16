import pandas as pd
from pathlib import Path

files = [
    "data/market_data.csv",
    "data/gpu_data.csv",
    "data/rpct_scores.csv",
    "data/provider_rankings.csv",
    "data/provider_marketshare.csv",
    "data/provider_concentration.csv",
    "data/alerts.csv"
]

score = 0
total = len(files)

for file in files:
    if Path(file).exists() and not pd.read_csv(file).empty:
        score += 1

quality_score = round(score / total * 100, 2)

pd.DataFrame([{
    "data_quality_score": quality_score,
    "files_ok": score,
    "files_total": total
}]).to_csv("data/data_quality.csv", index=False)

print("Data Quality:", quality_score)
