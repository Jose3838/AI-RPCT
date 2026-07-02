from __future__ import annotations

import json
from pathlib import Path

from copilot.intelligence.engine import get_unified_intelligence

ROOT = Path(__file__).resolve().parents[2]

DEFAULT_CONFIG = {
    "investment_score": {
        "historical": 0.15,
        "risk": 0.25,
        "forecast": 0.20,
        "pricing": 0.20,
        "capacity": 0.10,
        "market": 0.10,
    },
    "thresholds": {
        "buy_now": 80,
        "monitor": 60,
    },
}


def _load_decision_config() -> dict:
    path = ROOT / "config" / "decision_weights.json"

    if not path.exists():
        return DEFAULT_CONFIG

    with path.open(encoding="utf-8") as f:
        return json.load(f)


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


def _recommendation_from_score(score: int, thresholds: dict) -> str:
    buy_now = int(thresholds.get("buy_now", 80))
    monitor = int(thresholds.get("monitor", 60))

    if score >= buy_now:
        return "buy_now"

    if score >= monitor:
        return "monitor"

    return "wait"


def get_decision_score() -> dict:
    intelligence = get_unified_intelligence()
    config = _load_decision_config()
    weights = config["investment_score"]
    thresholds = config["thresholds"]

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
        (historical_score * weights.get("historical", 0))
        + (risk_score * weights.get("risk", 0))
        + (forecast_score * weights.get("forecast", 0))
        + (pricing_score * weights.get("pricing", 0))
        + (capacity_score * weights.get("capacity", 0))
        + (market_score * weights.get("market", 0))
    )

    recommendation = _recommendation_from_score(
        investment_score,
        thresholds,
    )

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
        "weights": weights,
        "thresholds": thresholds,
    }
