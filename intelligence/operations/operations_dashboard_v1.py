from intelligence.operations.collection_health import (
    collection_health
)

from intelligence.assets.historical_asset_health import (
    historical_asset_health
)

def operations_dashboard_v1():

    collection = collection_health()
    assets = historical_asset_health()

    return {
        "status": "ok",
        "version": "v1",
        "collection": collection,
        "historical_assets": {
            "score":
                assets.get(
                    "historical_asset_score",
                    0
                ),
            "healthy_assets":
                assets.get(
                    "healthy_assets",
                    0
                ),
            "growing_assets":
                assets.get(
                    "growing_or_healthy_assets",
                    0
                )
        }
    }
