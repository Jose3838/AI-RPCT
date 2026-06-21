import pandas as pd

FILE = "data/live_offers/provider_live_offer_history.csv"

def cheapest_gpu_leaderboard():

    df = pd.read_csv(FILE)

    latest_ts = df["observed_at"].max()

    latest = df[
        df["observed_at"] == latest_ts
    ]

    results = []

    for gpu in latest["gpu_model"].dropna().unique():

        gpu_df = latest[
            latest["gpu_model"] == gpu
        ]

        gpu_df = gpu_df.copy()

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

        results.append({
            "gpu_model": gpu,
            "provider": cheapest["provider"],
            "best_price":
                float(
                    cheapest[
                        "price_usd_per_gpu_hour"
                    ]
                )
        })

    return sorted(
        results,
        key=lambda x: x["best_price"]
    )
