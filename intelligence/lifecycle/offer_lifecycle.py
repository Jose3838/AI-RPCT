import pandas as pd

FILE = (
    "data/live_offers/"
    "provider_live_offer_history.csv"
)

def detect_offer_changes():

    df = pd.read_csv(FILE)

    timestamps = sorted(
        df["observed_at"].unique()
    )

    if len(timestamps) < 2:
        return {
            "new": 0,
            "removed": 0
        }

    current = df[
        df["observed_at"]
        == timestamps[-1]
    ]

    previous = df[
        df["observed_at"]
        == timestamps[-2]
    ]

    current_ids = set(
        current["fingerprint"]
    )

    previous_ids = set(
        previous["fingerprint"]
    )

    return {
        "new":
            len(
                current_ids
                - previous_ids
            ),

        "removed":
            len(
                previous_ids
                - current_ids
            )
    }
