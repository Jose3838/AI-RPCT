import pandas as pd
from pathlib import Path

path = Path("data/live_provider_data.csv")

if path.exists() and path.stat().st_size > 1:
    df = pd.read_csv(path)
else:
    df = pd.DataFrame(columns=["gpu", "price_per_hour"])

if df.empty:
    summary = pd.DataFrame(columns=[
        "gpu",
        "offers",
        "avg_price",
        "min_price",
        "max_price"
    ])
else:
    summary = df.groupby("gpu").agg(
        offers=("gpu", "count"),
        avg_price=("price_per_hour", "mean"),
        min_price=("price_per_hour", "min"),
        max_price=("price_per_hour", "max")
    ).reset_index()

summary["avg_price"] = summary["avg_price"].round(4)
summary["min_price"] = summary["min_price"].round(4)
summary["max_price"] = summary["max_price"].round(4)

summary.to_csv("data/live_offer_summary.csv", index=False)

print(summary.head())
