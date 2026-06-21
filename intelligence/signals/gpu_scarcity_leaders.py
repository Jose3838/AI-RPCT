import pandas as pd

FILE = "data/live_offers/provider_live_offer_history.csv"

def gpu_scarcity_leaders():

    df = pd.read_csv(FILE)

    counts = (
        df["gpu_model"]
        .value_counts()
        .sort_values()
    )

    return [
        {
            "gpu_model": gpu,
            "observations": int(count)
        }
        for gpu, count in counts.head(10).items()
    ]
