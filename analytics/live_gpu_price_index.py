import pandas as pd

df = pd.read_csv("data/live_provider_data.csv")

price_index = round(
    df["price_per_hour"].mean(),
    4
)

out = pd.DataFrame([{
    "gpu_price_index": price_index,
    "offers": len(df)
}])

out.to_csv(
    "data/live_gpu_price_index.csv",
    index=False
)

print(out)
