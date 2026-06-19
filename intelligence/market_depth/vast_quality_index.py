import pandas as pd

FILE = "data/live_offers/provider_live_offer_history.csv"

def vast_quality_index():

    df = pd.read_csv(FILE)

    vast = df[df["provider"] == "vast"]

    if len(vast) == 0:
        return {"status": "no_vast_data"}

    prices = pd.to_numeric(
        vast["price_usd_per_gpu_hour"],
        errors="coerce"
    ).dropna()

    return {
        "provider": "vast",
        "observations": int(len(vast)),
        "gpu_models": int(vast["gpu_model"].nunique()),
        "regions": int(vast["region"].nunique()),
        "min_price": round(float(prices.min()), 4) if len(prices) else None,
        "avg_price": round(float(prices.mean()), 4) if len(prices) else None,
        "max_price": round(float(prices.max()), 4) if len(prices) else None
    }
