from intelligence.assets.data_asset_growth import (
    data_asset_growth
)

def intelligence_score_v1():

    growth = data_asset_growth()

    mb = growth[
        "asset_size_mb"
    ]

    score = min(
        100,
        round(
            mb * 10,
            2
        )
    )

    return {
        "intelligence_score": score
    }
