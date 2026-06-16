import pandas as pd

gpu = pd.read_csv("data/gpu_data.csv")

health = (
    gpu.groupby("provider")
    .agg({
        "gpu": "count",
        "price_per_hour": "mean",
        "availability": "mean"
    })
    .reset_index()
)

health["status"] = health["gpu"].apply(
    lambda x: "OK" if x > 0 else "NO_DATA"
)

health.to_csv("data/provider_health.csv", index=False)

print(health)
