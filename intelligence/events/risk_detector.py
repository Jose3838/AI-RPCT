import pandas as pd

FILE = "data/feature_store/gpu_market_depth_history.csv"

def risk_detector():

    df = pd.read_csv(FILE)

    risks = []

    for gpu in df["gpu_model"].unique():

        gpu_df = df[
            df["gpu_model"] == gpu
        ]

        if len(gpu_df) < 3:
            continue

        latest = float(
            gpu_df.iloc[-1]["offer_count"]
        )

        avg_count = (
            gpu_df["offer_count"]
            .astype(float)
            .mean()
        )

        if latest < avg_count * 0.8:

            risks.append({
                "gpu_model": gpu,
                "latest_supply": latest,
                "historical_supply":
                    round(
                        avg_count,
                        2
                    )
            })

    return risks
