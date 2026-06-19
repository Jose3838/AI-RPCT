import pandas as pd

FILE = "data/live_offers/provider_live_offer_history.csv"

def live_provider_mix():

    df = pd.read_csv(FILE)

    provider_counts = (
        df["provider"]
        .value_counts()
        .to_dict()
    )

    total = len(df)

    return {
        "total_observations": total,
        "provider_mix": {
            provider: round(
                count / total,
                4
            )
            for provider, count
            in provider_counts.items()
        }
    }
