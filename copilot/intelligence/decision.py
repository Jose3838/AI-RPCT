from __future__ import annotations

from copilot.intelligence.engine import get_unified_intelligence


def _score_from_risk(risk_summary: dict) -> int:
    risk_score = risk_summary.get("risk_score")

    try:
        value = int(float(risk_score))
    except (TypeError, ValueError):
        return 50

    return max(0, min(100, value))


def _score_from_forecast(forecast_summary: dict) -> int:
    watch_count = forecast_summary.get("watch_count", 0)

    try:
        watches = int(float(watch_count))
    except (TypeError, ValueError):
        watches = 0

    if watches == 0:
        return 80

    if watches <= 2:
        return 65

    return 45


def _score_from_pricing(pricing_summary: dict) -> int:
    price_history = pricing_summary.get("live_price_history_records", 0)

    try:
        records = int(float(price_history))
    except (TypeError, ValueError):
        records = 0

    if records >= 20:
        return 75

    if records >= 5:
        return 60

    return 45


def get_decision_score() -> dict:
    intelligence = get_unified_intelligence()

    risk_score = _score_from_risk(
        intelligence["risk"].get("summary", {})
    )
    forecast_score = _score_from_forecast(
        intelligence["forecast"].get("summary", {})
    )
    pricing_score = _score_from_pricing(
        intelligence["pricing"].get("summary", {})
    )

    investment_score = round(
        (risk_score * 0.4)
        + (forecast_score * 0.3)
        + (pricing_score * 0.3)
    )

    if investment_score >= 80:
        recommendation = "buy_now"
    elif investment_score >= 60:
        recommendation = "monitor"
    else:
        recommendation = "wait"

    return {
        "summary": {
            "status": "decision score available",
            "investment_score": investment_score,
            "recommendation": recommendation,
        },
        "scores": {
            "risk_score": risk_score,
            "forecast_score": forecast_score,
            "pricing_score": pricing_score,
        },
        "weights": {
            "risk": 0.4,
            "forecast": 0.3,
            "pricing": 0.3,
        },
    }
