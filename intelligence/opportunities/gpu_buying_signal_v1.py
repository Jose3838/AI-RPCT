from intelligence.opportunities.gpu_opportunity_ranking_v1 import (
    gpu_opportunity_ranking_v1
)


def gpu_buying_signal_v1():

    opportunities = gpu_opportunity_ranking_v1()

    signals = []

    for item in opportunities:

        discount = float(
            item.get("discount_pct", 0)
        )

        if discount >= 25:
            signal = "BUY"
            confidence = "high"
        elif discount >= 10:
            signal = "WATCH"
            confidence = "medium"
        else:
            signal = "AVOID"
            confidence = "low"

        signals.append({
            "gpu_model": item.get("gpu_model"),
            "signal": signal,
            "confidence": confidence,
            "avg_price": item.get("avg_price"),
            "best_price": item.get("best_price"),
            "discount_pct": item.get("discount_pct")
        })

    return {
        "status": "ok",
        "version": "v1",
        "signals": signals
    }
