import pandas as pd

FILE = "data/live_offers/provider_live_offer_history.csv"

def snapshot_integrity():

    df = pd.read_csv(FILE)

    if len(df) == 0:
        return {
            "status": "empty_dataset"
        }

    return {
        "rows": int(len(df)),
        "providers": int(df["provider"].nunique()),
        "gpu_models": int(df["gpu_model"].nunique()),
        "null_prices": int(
            df["price_usd_per_gpu_hour"]
            .isna()
            .sum()
        )
    }
