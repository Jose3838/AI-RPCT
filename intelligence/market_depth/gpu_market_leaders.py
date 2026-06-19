import pandas as pd

FILE = "data/live_offers/provider_live_offer_history.csv"

def gpu_market_leaders():

    df = pd.read_csv(FILE)

    result = []

    for gpu in df["gpu_model"].dropna().unique():

        gpu_df = df[
            df["gpu_model"] == gpu
        ]

        leader = (
            gpu_df["provider"]
            .value_counts()
            .idxmax()
        )

        observations = (
            gpu_df["provider"]
            .value_counts()
            .max()
        )

        result.append({
            "gpu_model": gpu,
            "leader": leader,
            "observations":
                int(observations)
        })

    return sorted(
        result,
        key=lambda x:x["observations"],
        reverse=True
    )
