from intelligence.events.opportunity_detector import (
    opportunity_detector
)

from intelligence.events.risk_detector import (
    risk_detector
)

def daily_alpha_feed():

    return {
        "opportunities":
            opportunity_detector(),

        "risks":
            risk_detector()
    }
