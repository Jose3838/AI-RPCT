import pandas as pd

FILE = "data/live_offers/provider_live_offer_history.csv"

def detect_supply_shock():

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

    shocks = []

    for provider in current["provider"].unique():

        c = len(
            current[
                current["provider"] == provider
            ]
        )

        p = len(
            previous[
                previous["provider"] == provider
            ]
        )

        if p == 0:
            continue

        change = (c-p)/p

        if abs(change) > 0.30:

            shocks.append({
                "provider": provider,
                "change_pct":
                    round(change*100,2)
            })

    return shocks
