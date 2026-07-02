from __future__ import annotations

from copilot.intelligence.engine import get_unified_intelligence


def _clamp_score(value: int) -> int:
    return max(0, min(100, value))


def _score_from_risk(risk_summary: dict) -> int:
    risk_score = risk_summary.get("risk_score")

    try:
        value = int(float(risk_score))
    except (TypeError, ValueError):
        return 50

    return _clamp_score(value)


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


def _score_from_historical(historical_summary: dict) -> int:
    years_covered = historical_summary.get("years_covered", 0)
    source_records = historical_summary.get("source_records", 0)

    try:
        years = int(float(years_covered))
        sources = int(float(source_records))
    except (TypeError, ValueError):
        return 50

    if years >= 10 and sources >= 15:
        return 80

    if years >= 5:
        return 65

    return 45


def _score_from_capacity(capacity_summary: dict) -> int:
    capacity_records = capacity_summary.get("capacity_records", 0)

    try:
        records = int(float(capacity_records))
    except (TypeError, ValueError):
        return 50

    if records >= 10:
        return 75

    if records >= 3:
        return 60

    return 45


def _score_from_market(market_summary: dict) -> int:
    market_records = (
        market_summary.get("market_brief_records", 0)
        + market_summary.get("market_mover_records", 0)
        + market_summary.get("frontier_index_records", 0)
        + market_summary.get("category_index_records", 0)
        + market_summary.get("watchlist_records", 0)
    )

    try:
        records = int(float(market_records))
    except (TypeError, ValueError):
        return 50

    if records >= 20:
        return 75

    if records >= 5:
        return 60

    return 45


def _recommendation_from_score(score: int) -> str:
    if score >= 80:
        return "buy_now"

    if score >= 60:
        return "monitor"

    return "wait"


def get_decision_score() -> dict:
    intelligence = get_unified_intelligence()

    historical_score = _score_from_historical(
        intelligence["historical"].get("summary", {})
    )
    risk_score = _score_from_risk(
        intelligence["risk"].get("summary", {})
    )
    forecast_score = _score_from_forecast(
        intelligence["forecast"].get("summary", {})
    )
    pricing_score = _score_from_pricing(
        intelligence["pricing"].get("summary", {})
    )
    capacity_score = _score_from_capacity(
        intelligence["capacity"].get("summary", {})
    )
    market_score = _score_from_market(
        intelligence["market"].get("summary", {})
    )

    investment_score = round(
        (historical_score * 0.15)
        + (risk_score * 0.25)
        + (forecast_score * 0.20)
        + (pricing_score * 0.20)
        + (capacity_score * 0.10)
        + (market_score * 0.10)
    )

    recommendation = _recommendation_from_score(investment_score)

    return {
        "summary": {
            "status": "decision score available",
            "investment_score": investment_score,
            "recommendation": recommendation,
        },
        "scores": {
            "historical_score": historical_score,
            "risk_score": risk_score,
            "forecast_score": forecast_score,
            "pricing_score": pricing_score,
            "capacity_score": capacity_score,
            "market_score": market_score,
        },
        "weights": {
            "historical": 0.15,
            "risk": 0.25,
            "forecast": 0.20,
            "pricing": 0.20,
            "capacity": 0.10,
            "market": 0.10,
        },
    }
