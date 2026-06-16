import pandas as pd

df = pd.read_csv(
    "data/provider_marketshare.csv"
)

hhi = (
    (df["market_share"] ** 2)
    .sum()
)

print("HHI:", round(hhi,2))

pd.DataFrame([
    {"hhi": hhi}
]).to_csv(
    "data/provider_concentration.csv",
    index=False
)
