import pandas as pd
from pathlib import Path

watchlist = pd.read_csv("data/gpu_watchlist.csv")
summary = pd.read_csv("data/live_offer_summary.csv")

df = watchlist.merge(
    summary,
    on="gpu",
    how="left"
)

df["tracked"] = df["offers"].notna()
df["offers"] = df["offers"].fillna(0).astype(int)
df["avg_price"] = df["avg_price"].fillna(0)
df["min_price"] = df["min_price"].fillna(0)
df["max_price"] = df["max_price"].fillna(0)

df.to_csv("data/gpu_watchlist_intelligence.csv", index=False)

print(df)
