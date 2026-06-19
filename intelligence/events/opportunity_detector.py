import pandas as pd

FILE = "data/feature_store/gpu_market_depth_history.csv"

def opportunity_detector():

    df = pd.read_csv(FILE)

    opportunities = []

    for gpu in df["gpu_model"].unique():

        gpu_df = df[
            df["gpu_model"] == gpu
        ]

        if len(gpu_df) < 3:
            continue

        latest = float(
            gpu_df.iloc[-1]["avg_price"]
        )

        historical = (
            gpu_df["avg_price"]
            .astype(float)
            .mean()
        )

        if latest < historical * 0.9:

            opportunities.append({
                "gpu_model": gpu,
                "latest_price": latest,
                "historical_avg":
                    round(
                        historical,
                        4
                    )
            })

    return opportunities
