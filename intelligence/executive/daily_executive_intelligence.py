from intelligence.events.opportunity_detector import (
    opportunity_detector
)

from intelligence.events.risk_detector import (
    risk_detector
)

from intelligence.signals.provider_concentration_risk import (
    provider_concentration_risk
)

def daily_executive_intelligence():

    return {
        "opportunities":
            opportunity_detector(),

        "risks":
            risk_detector(),

        "provider_concentration":
            provider_concentration_risk()
    }
