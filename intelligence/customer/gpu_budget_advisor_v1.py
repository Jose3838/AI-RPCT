from intelligence.opportunities.gpu_buying_signal_v1 import (
    gpu_buying_signal_v1
)


def gpu_budget_advisor_v1():
    signals = gpu_buying_signal_v1().get("signals", [])

    buy = [
        item for item in signals
        if item.get("signal") == "BUY"
    ]

    watch = [
        item for item in signals
        if item.get("signal") == "WATCH"
    ]

    if buy:
        best = sorted(
            buy,
            key=lambda x: x.get("discount_pct", 0),
            reverse=True
        )[0]

        decision = "buy_now"
        reason = (
            f"{best.get('gpu_model')} has the strongest discount "
            f"at {best.get('discount_pct')}% below average."
        )

    elif watch:
        best = sorted(
            watch,
            key=lambda x: x.get("discount_pct", 0),
            reverse=True
        )[0]

        decision = "watch"
        reason = (
            f"{best.get('gpu_model')} is close to a buy signal "
            f"with {best.get('discount_pct')}% discount."
        )

    else:
        best = None
        decision = "wait"
        reason = "No strong GPU buying opportunity detected."

    return {
        "status": "ok",
        "version": "v1",
        "decision": decision,
        "best_candidate": best,
        "reason": reason,
        "buy_count": len(buy),
        "watch_count": len(watch)
    }
