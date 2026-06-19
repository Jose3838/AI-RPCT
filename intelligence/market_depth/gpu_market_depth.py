import pandas as pd

FILE = "data/live_offers/provider_live_offer_history.csv"


def gpu_market_depth():

    df = pd.read_csv(FILE)

    if len(df) == 0:
        return []

    df["observed_at"] = pd.to_datetime(
        df["observed_at"],
        errors="coerce"
    )

    latest_time = df["observed_at"].max()

    # Treat all offers observed within the latest 10 minutes as one market snapshot.
    window_start = latest_time - pd.Timedelta(minutes=10)

    latest = df[
        df["observed_at"] >= window_start
    ]

    results = []

    for gpu in sorted(
        latest["gpu_model"]
        .dropna()
        .unique()
    ):

        gpu_df = latest[
            latest["gpu_model"] == gpu
        ].copy()

        prices = pd.to_numeric(
            gpu_df["price_usd_per_gpu_hour"],
            errors="coerce"
        ).dropna()

        if len(prices) == 0:
            continue

        results.append({
            "gpu_model": gpu,
            "offer_count": int(len(gpu_df)),
            "min_price": round(float(prices.min()), 4),
            "avg_price": round(float(prices.mean()), 4),
            "max_price": round(float(prices.max()), 4)
        })

    return sorted(
        results,
        key=lambda x: x["offer_count"],
        reverse=True
    )
