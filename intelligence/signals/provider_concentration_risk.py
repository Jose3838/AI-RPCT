import pandas as pd

FILE = "data/live_offers/provider_live_offer_history.csv"

def provider_concentration_risk():

    df = pd.read_csv(FILE)

    total = len(df)

    if total == 0:
        return {
            "risk": "unknown"
        }

    shares = (
        df["provider"]
        .value_counts(normalize=True)
        .to_dict()
    )

    largest = max(
        shares.values()
    )

    if largest > 0.80:
        risk = "high"

    elif largest > 0.60:
        risk = "medium"

    else:
        risk = "low"

    return {
        "risk": risk,
        "largest_provider_share":
            round(
                largest,
                4
            ),
        "shares": shares
    }
