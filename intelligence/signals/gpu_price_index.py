import pandas as pd

FILE = "data/live_offers/provider_live_offer_history.csv"

def calculate_gpu_price_index():

    df = pd.read_csv(FILE)

    if len(df) == 0:
        return None

    latest_ts = df["observed_at"].max()

    latest = df[df["observed_at"] == latest_ts]

    prices = pd.to_numeric(
        latest["price_usd_per_gpu_hour"],
        errors="coerce"
    )

    prices = prices.dropna()

    if len(prices) == 0:
        return None

    return {
        "timestamp": latest_ts,
        "gpu_price_index": round(
            prices.mean(),
            4
        ),
        "min_price": round(prices.min(),4),
        "max_price": round(prices.max(),4),
        "offer_count": len(prices)
    }
