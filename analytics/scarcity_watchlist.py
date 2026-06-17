import pandas as pd

df = pd.read_csv("data/gpu_watchlist_intelligence.csv")

scarce = df[
    (df["tracked"] == False) |
    (df["offers"] <= 2)
].copy()

scarce["scarcity_flag"] = True

scarce.to_csv("data/scarcity_watchlist.csv", index=False)

print(scarce)
