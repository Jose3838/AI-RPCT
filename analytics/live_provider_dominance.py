import pandas as pd

df = pd.read_csv("data/live_provider_market_share.csv")

top = df.sort_values(
    "market_share_pct",
    ascending=False
).iloc[0]

out = pd.DataFrame([{
    "dominant_provider": top["provider"],
    "dominance_pct": top["market_share_pct"]
}])

out.to_csv("data/live_provider_dominance.csv", index=False)

print(out)
