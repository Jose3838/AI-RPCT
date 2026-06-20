from intelligence.investor.investor_readiness_score import investor_readiness_score
from intelligence.signals.data_moat_score_v2 import data_moat_score_v2
from intelligence.forecast.forecast_accuracy_trend import forecast_accuracy_trend
from intelligence.operations.collection_health import collection_health


def executive_scorecard_v1():
    investor = investor_readiness_score()
    moat = data_moat_score_v2()
    forecast = forecast_accuracy_trend()
    collection = collection_health()

    score = round(
        float(investor.get("investor_readiness_score", 0)) * 0.35
        + float(moat.get("data_moat_score", 0)) * 0.30
        + float(forecast.get("forecast_quality_score", 0)) * 0.25
        + (100 if collection.get("healthy") else 0) * 0.10,
        2
    )

    if score >= 80:
        level = "strong_terminal"
    elif score >= 60:
        level = "credible_intelligence_product"
    elif score >= 40:
        level = "early_intelligence_product"
    else:
        level = "prototype"

    return {
        "status": "ok",
        "version": "v1",
        "executive_score": score,
        "executive_level": level,
        "components": {
            "investor_readiness_score": investor.get("investor_readiness_score", 0),
            "data_moat_score": moat.get("data_moat_score", 0),
            "forecast_quality_score": forecast.get("forecast_quality_score", 0),
            "collection_healthy": collection.get("healthy", False)
        },
        "readout": (
            f"AI-RPCT is a {level} with executive score {score}."
        )
    }
