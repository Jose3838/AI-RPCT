from intelligence.signals.market_supply_index import (
    calculate_market_supply_index
)

from intelligence.signals.gpu_price_index import (
    calculate_gpu_price_index
)

from intelligence.signals.capacity_churn_index import (
    calculate_capacity_churn
)

def forecast_feature_snapshot():

    return {
        "market_supply":
            calculate_market_supply_index(),

        "gpu_price":
            calculate_gpu_price_index(),

        "capacity_churn":
            calculate_capacity_churn()
    }
