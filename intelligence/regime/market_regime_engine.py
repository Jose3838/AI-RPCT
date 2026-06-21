import pandas as pd

FILE = "data/live_offers/provider_live_offer_history.csv"

def market_regime_engine():

    df = pd.read_csv(FILE)

    observations = len(df)

    providers = df["provider"].nunique()

    gpu_models = df["gpu_model"].nunique()

    if observations < 1000:
        regime = "Data Accumulation"

    elif providers <= 2:
        regime = "Provider Concentrated"

    elif gpu_models >= 20:
        regime = "Broad Market"

    else:
        regime = "Expansion"

    return {
        "regime": regime,
        "observations": observations,
        "providers": providers,
        "gpu_models": gpu_models
    }
