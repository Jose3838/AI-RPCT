from infrastructure_risk_signal import (
    build_infrastructure_risk_signal
)
from provider_concentration_risk import (
    build_provider_concentration_risk
)
from forecast_accuracy_v2 import (
    build_forecast_accuracy_v2
)
from data_trust_index import (
    build_data_trust_index
)


def build_executive_risk_dashboard():

    infra = build_infrastructure_risk_signal()
    concentration = build_provider_concentration_risk()
    accuracy = build_forecast_accuracy_v2()
    trust = build_data_trust_index()

    return {
        "status": "ok",
        "version": "v1",
        "infrastructure_risk":
            infra["risk_level"],
        "provider_concentration_risk":
            concentration.get(
                "concentration_risk",
                "unknown"
            ),
        "forecast_accuracy":
            accuracy.get(
                "direction_accuracy",
                0
            ),
        "data_trust_index":
            trust["data_trust_index"]
    }
