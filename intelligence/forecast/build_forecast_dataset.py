import pandas as pd

FILE = "data/live_offers/provider_live_offer_history.csv"

def build_forecast_dataset():

    df = pd.read_csv(FILE)

    return {
        "rows": len(df),
        "providers":
            df["provider"].nunique(),
        "gpu_models":
            df["gpu_model"].nunique()
    }
