from intelligence.assets.data_asset_velocity import (
    data_asset_velocity
)

from intelligence.forecast.forecast_accuracy_engine_v4 import (
    forecast_accuracy_engine_v4
)

from intelligence.regime.market_regime_engine import (
    market_regime_engine
)

def daily_intelligence_snapshot_v5():

    return {
        "asset_velocity":
            data_asset_velocity(),

        "forecast_accuracy":
            forecast_accuracy_engine_v4(),

        "market_regime":
            market_regime_engine()
    }
