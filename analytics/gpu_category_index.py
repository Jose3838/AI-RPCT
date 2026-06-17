import pandas as pd

df = pd.read_csv("data/gpu_watchlist_intelligence.csv")

category_index = df.groupby("category").agg(
    gpu_count=("gpu", "count"),
    tracked_gpus=("tracked", "sum"),
    total_offers=("offers", "sum"),
    avg_price=("avg_price", "mean")
).reset_index()

category_index["avg_price"] = category_index["avg_price"].round(4)

category_index.to_csv("data/gpu_category_index.csv", index=False)

print(category_index)
