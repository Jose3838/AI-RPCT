import pandas as pd

FILE = "data/live_offers/provider_live_offer_history.csv"

def detect_new_gpu_entries():

    df = pd.read_csv(FILE)

    timestamps = sorted(
        df["observed_at"].unique()
    )

    if len(timestamps) < 2:
        return []

    current = df[
        df["observed_at"] == timestamps[-1]
    ]

    previous = df[
        df["observed_at"] == timestamps[-2]
    ]

    old_gpus = set(
        previous["gpu_model"]
        .dropna()
        .unique()
    )

    new_gpus = set(
        current["gpu_model"]
        .dropna()
        .unique()
    )

    return list(
        new_gpus - old_gpus
    )
