from intelligence.signals.market_breadth_index import (
    market_breadth_index
)

from intelligence.signals.provider_concentration_risk import (
    provider_concentration_risk
)

from intelligence.signals.data_moat_growth_rate import (
    data_moat_growth_rate
)

def market_intelligence_scorecard():

    return {
        "breadth":
            market_breadth_index(),

        "concentration":
            provider_concentration_risk(),

        "data_moat":
            data_moat_growth_rate()
    }
