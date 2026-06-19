import pandas as pd

FILE = "data/live_offers/provider_live_offer_history.csv"

def best_price_per_gpu():

    df = pd.read_csv(FILE)

    latest_ts = df["observed_at"].max()

    latest = df[
        df["observed_at"] == latest_ts
    ]

    result = []

    for gpu in latest["gpu_model"].unique():

        gpu_df = latest[
            latest["gpu_model"] == gpu
        ]

        gpu_df["price_usd_per_gpu_hour"] = pd.to_numeric(
            gpu_df["price_usd_per_gpu_hour"],
            errors="coerce"
        )

        gpu_df = gpu_df.dropna(
            subset=["price_usd_per_gpu_hour"]
        )

        if len(gpu_df) == 0:
            continue

        cheapest = gpu_df.loc[
            gpu_df[
                "price_usd_per_gpu_hour"
            ].idxmin()
        ]

        result.append({
            "gpu_model": gpu,
            "provider": cheapest["provider"],
            "best_price":
                cheapest["price_usd_per_gpu_hour"]
        })

    return result
