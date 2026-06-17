import pandas as pd

df = pd.read_csv(
    "data/provider_marketshare.csv"
)

dominance = df["market_share"].max()

out = pd.DataFrame([{
    "provider_dominance_index": round(dominance, 2)
}])

out.to_csv(
    "data/provider_dominance_index.csv",
    index=False
)

print(out)
