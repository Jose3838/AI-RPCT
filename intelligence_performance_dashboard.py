from forecast_accuracy_v2 import build_forecast_accuracy_v2
from forecast_error_tracking import build_forecast_error_tracking
from forecast_weight_optimization import build_forecast_weight_optimization
from data_moat_dashboard import build_data_moat_dashboard
from data_trust_index import build_data_trust_index


def build_intelligence_performance_dashboard():
    accuracy = build_forecast_accuracy_v2()
    errors = build_forecast_error_tracking()
    optimization = build_forecast_weight_optimization()
    moat = build_data_moat_dashboard()
    trust = build_data_trust_index()

    return {
        "status": "ok",
        "version": "v1",
        "forecast_accuracy": accuracy.get(
            "direction_accuracy",
            0
        ),
        "forecast_error_rate": errors.get(
            "error_rate",
            0
        ),
        "weighting_strategy": optimization.get(
            "weighting_strategy",
            "unknown"
        ),
        "data_moat_score": moat.get(
            "data_moat_score",
            0
        ),
        "data_trust_index": trust.get(
            "data_trust_index",
            0
        )
    }
