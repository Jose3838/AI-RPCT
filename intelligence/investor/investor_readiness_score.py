from intelligence.signals.data_moat_score_v2 import data_moat_score_v2
from intelligence.forecast.forecast_accuracy_trend import forecast_accuracy_trend
from intelligence.operations.collection_health import collection_health


def investor_readiness_score():
    moat = data_moat_score_v2()
    forecast = forecast_accuracy_trend()
    collection = collection_health()

    moat_score = float(moat.get("data_moat_score", 0))
    forecast_score = float(forecast.get("forecast_quality_score", 0))
    collection_score = 100 if collection.get("healthy") else 0

    score = round(
        moat_score * 0.45
        + forecast_score * 0.35
        + collection_score * 0.20,
        2
    )

    if score >= 80:
        level = "investor_ready"
    elif score >= 60:
        level = "promising"
    elif score >= 40:
        level = "early_but_validating"
    else:
        level = "too_early"

    return {
        "status": "ok",
        "version": "v1",
        "investor_readiness_score": score,
        "investor_readiness_level": level,
        "components": {
            "data_moat_score": moat_score,
            "forecast_quality_score": forecast_score,
            "collection_score": collection_score
        },
        "signals": {
            "data_moat": moat,
            "forecast_trend": forecast,
            "collection_health": collection
        }
    }
