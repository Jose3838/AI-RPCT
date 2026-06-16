import pandas as pd
from pathlib import Path

path = Path("data/provider_rankings.csv")

if not path.exists():
    raise FileNotFoundError("data/provider_rankings.csv not found. Run analytics/provider_rankings.py first.")

df = pd.read_csv(path)

total = df["score"].sum()

if total == 0:
    df["market_share"] = 0
else:
    df["market_share"] = df["score"] / total * 100

df.to_csv("data/provider_marketshare.csv", index=False)

print(df[["provider", "market_share"]])
