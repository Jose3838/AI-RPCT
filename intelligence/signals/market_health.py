from intelligence.signals.provider_concentration_risk import (
    provider_concentration_risk
)

from intelligence.signals.market_breadth_index import (
    market_breadth_index
)

def market_health():

    concentration = provider_concentration_risk()
    breadth = market_breadth_index()

    score = 100

    if concentration["risk"] == "high":
        score -= 30

    if breadth["gpu_markets"] < 10:
        score -= 20

    return {
        "score": score,
        "concentration": concentration,
        "breadth": breadth
    }
