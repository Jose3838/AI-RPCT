from forecast_accuracy_v2 import build_forecast_accuracy_v2
from data_trust_index import build_data_trust_index
from historical_intelligence_score import build_historical_intelligence_score


def build_intelligence_quality_dashboard():
    accuracy = build_forecast_accuracy_v2()
    trust = build_data_trust_index()
    history = build_historical_intelligence_score()

    return {
        "status": "ok",
        "version": "v1",
        "forecast_accuracy": accuracy,
        "data_trust": trust,
        "historical_intelligence": history,
        "quality_signal": (
            "institutional_grade"
            if trust["data_trust_index"] >= 90
            and accuracy.get("direction_accuracy", 0) >= 70
            else "improving_intelligence"
        )
    }
