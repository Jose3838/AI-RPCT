import pandas as pd

FILE = "data/live_offers/provider_live_offer_history.csv"


def provider_supply_share(minutes=10):

    df = pd.read_csv(FILE)

    if df.empty:
        return []

    df["observed_at"] = pd.to_datetime(
        df["observed_at"],
        errors="coerce",
        utc=True
    )

    df = df.dropna(
        subset=["observed_at", "provider"]
    )

    if df.empty:
        return []

    latest_time = df["observed_at"].max()

    window_start = latest_time - pd.Timedelta(
        minutes=minutes
    )

    latest = df[
        df["observed_at"] >= window_start
    ]

    total = len(latest)

    result = []

    for provider in sorted(latest["provider"].unique()):

        provider_df = latest[
            latest["provider"] == provider
        ]

        rows = len(provider_df)
        market_share_pct = round(
            rows / max(total, 1) * 100,
            4
        )

        result.append({
            "provider": provider,
            "rows": rows,
            "market_share_pct": market_share_pct,
            "offer_share": round(
                rows / max(total, 1),
                4
            )
        })

    return sorted(
        result,
        key=lambda x: x["market_share_pct"],
        reverse=True
    )
