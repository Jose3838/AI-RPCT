import pandas as pd

df = pd.read_csv("data/gpu_watchlist_intelligence.csv")

frontier = df[df["category"] == "frontier"]

if frontier.empty:
    index = 0
    offers = 0
else:
    index = round(frontier["avg_price"].replace(0, pd.NA).dropna().mean(), 4)
    offers = int(frontier["offers"].sum())

out = pd.DataFrame([{
    "frontier_gpu_index": float(index) if index == index else 0,
    "frontier_offers": offers
}])

out.to_csv("data/frontier_gpu_index.csv", index=False)

print(out)
