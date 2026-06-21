from intelligence.opportunities.gpu_opportunity_ranking_v1 import (
    gpu_opportunity_ranking_v1
)

from intelligence.opportunities.gpu_buying_signal_v1 import (
    gpu_buying_signal_v1
)


def customer_value_dashboard_v1():

    opportunities = gpu_opportunity_ranking_v1()
    buying = gpu_buying_signal_v1()

    buy_signals = [
        item for item in buying.get("signals", [])
        if item.get("signal") == "BUY"
    ]

    watch_signals = [
        item for item in buying.get("signals", [])
        if item.get("signal") == "WATCH"
    ]

    avoid_signals = [
        item for item in buying.get("signals", [])
        if item.get("signal") == "AVOID"
    ]

    if buy_signals:
        recommendation = "buy_opportunities_available"
    elif watch_signals:
        recommendation = "watch_market"
    else:
        recommendation = "no_clear_buy_signal"

    return {
        "status": "ok",
        "version": "v1",
        "recommendation": recommendation,
        "buy_count": len(buy_signals),
        "watch_count": len(watch_signals),
        "avoid_count": len(avoid_signals),
        "top_opportunities": opportunities[:5],
        "buy_signals": buy_signals[:5],
        "watch_signals": watch_signals[:5],
        "readout": (
            f"{len(buy_signals)} BUY signals and "
            f"{len(watch_signals)} WATCH signals detected."
        )
    }
