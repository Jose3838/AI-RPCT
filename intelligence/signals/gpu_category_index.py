import pandas as pd

from intelligence.catalog.gpu_categories import (
    GPU_CATEGORY_MAP
)

FILE = "data/live_offers/provider_live_offer_history.csv"

def category_supply_index():

    df = pd.read_csv(FILE)

    latest_ts = df["observed_at"].max()

    latest = df[
        df["observed_at"] == latest_ts
    ]

    result = {}

    for gpu, category in GPU_CATEGORY_MAP.items():

        count = len(
            latest[
                latest["gpu_model"]
                .astype(str)
                .str.contains(gpu, case=False)
            ]
        )

        result[category] = (
            result.get(category,0)
            + count
        )

    return result
