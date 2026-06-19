import pandas as pd

FILE = "data/live_offers/provider_live_offer_history.csv"

def detect_provider_expansion():

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

    events = []

    for provider in current["provider"].unique():

        c = current[
            current["provider"] == provider
        ]

        p = previous[
            previous["provider"] == provider
        ]

        if len(c) > len(p):
            events.append({
                "provider": provider,
                "event": "supply_expansion",
                "delta": len(c)-len(p)
            })

    return events
