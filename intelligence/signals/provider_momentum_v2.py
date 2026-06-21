import pandas as pd

FILE = "data/live_offers/provider_live_offer_history.csv"

def calculate_provider_momentum_v2():

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

    results = []

    for provider in current["provider"].unique():

        c = current[current["provider"] == provider]
        p = previous[previous["provider"] == provider]

        score = (
            len(c)
            - len(p)
        )

        results.append({
            "provider": provider,
            "momentum_score": score
        })

    return sorted(
        results,
        key=lambda x:x["momentum_score"],
        reverse=True
    )
