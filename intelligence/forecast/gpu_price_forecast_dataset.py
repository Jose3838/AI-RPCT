import pandas as pd

FILE = "data/live_offers/provider_live_offer_history.csv"

def gpu_price_forecast_dataset():

    df = pd.read_csv(FILE)

    result = []

    for gpu in sorted(df["gpu_model"].dropna().unique()):

        gpu_df = df[
            df["gpu_model"] == gpu
        ]

        result.append({
            "gpu_model": gpu,
            "observations": len(gpu_df),
            "avg_price":
                round(
                    gpu_df[
                        "price_usd_per_gpu_hour"
                    ].astype(float).mean(),
                    4
                )
        })

    return result
