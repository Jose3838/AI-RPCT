import pandas as pd

FILE = "data/live_offers/provider_live_offer_history.csv"

def provider_supply_share():

    df = pd.read_csv(FILE)

    latest_ts = df["observed_at"].max()

    latest = df[df["observed_at"] == latest_ts]

    total = len(latest)

    result = []

    for provider in latest["provider"].unique():

        provider_df = latest[
            latest["provider"] == provider
        ]

        result.append({
            "provider": provider,
            "offer_share": round(
                len(provider_df) / max(total,1),
                4
            )
        })

    return sorted(
        result,
        key=lambda x:x["offer_share"],
        reverse=True
    )
