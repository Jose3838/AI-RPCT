import pandas as pd

FILE = "data/live_offers/provider_live_offer_history.csv"

def market_breadth_index():

    df = pd.read_csv(FILE)

    unique_gpus = (
        df["gpu_model"]
        .dropna()
        .nunique()
    )

    return {
        "gpu_markets":
            int(unique_gpus)
    }
