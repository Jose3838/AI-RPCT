import pandas as pd

FILE = "data/live_offers/provider_live_offer_history.csv"

def gpu_leaderboard():

    df = pd.read_csv(FILE)

    result = (
        df["gpu_model"]
        .value_counts()
        .head(20)
        .reset_index()
    )

    result.columns = [
        "gpu_model",
        "observations"
    ]

    return result.to_dict(
        orient="records"
    )
