import pandas as pd

df = pd.read_csv("data/live_offer_summary.csv")

most_expensive = df.sort_values(
    "avg_price",
    ascending=False
).head(10)

cheapest = df.sort_values(
    "avg_price",
    ascending=True
).head(10)

most_available = df.sort_values(
    "offers",
    ascending=False
).head(10)

most_expensive.to_csv(
    "data/live_gpu_most_expensive.csv",
    index=False
)

cheapest.to_csv(
    "data/live_gpu_cheapest.csv",
    index=False
)

most_available.to_csv(
    "data/live_gpu_most_available.csv",
    index=False
)

print("Most expensive")
print(most_expensive)

print("Cheapest")
print(cheapest)

print("Most available")
print(most_available)
