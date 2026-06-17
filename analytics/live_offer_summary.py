import pandas as pd

df = pd.read_csv("data/live_provider_data.csv")

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
