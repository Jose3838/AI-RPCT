import pandas as pd

FILE = "data/live_offers/provider_live_offer_history.csv"

def calculate_market_supply_index():

    df = pd.read_csv(FILE)

    if len(df) == 0:
        return None

    latest_ts = df["observed_at"].max()

    latest = df[df["observed_at"] == latest_ts]

    available = latest["available"].astype(bool).sum()

    total = len(latest)

    return {
        "timestamp": latest_ts,
        "available_offers": int(available),
        "total_offers": int(total),
        "supply_index": round(
            available / max(total,1),
            4
        )
    }
