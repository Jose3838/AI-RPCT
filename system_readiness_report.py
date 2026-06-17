from history_schema_health import build_history_schema_health
from data_trust_index import build_data_trust_index
from data_moat_dashboard import build_data_moat_dashboard
from intelligence_performance_dashboard import build_intelligence_performance_dashboard


def build_system_readiness_report():
    schema = build_history_schema_health()
    trust = build_data_trust_index()
    moat = build_data_moat_dashboard()
    performance = build_intelligence_performance_dashboard()

    timestamp_ready = all(
        item.get("timestamp_ready") is True
        for item in schema["files"]
    )

    return {
        "status": "ok",
        "version": "v1",
        "timestamp_ready": timestamp_ready,
        "data_trust_index": trust["data_trust_index"],
        "data_moat_score": moat["data_moat_score"],
        "forecast_accuracy": performance["forecast_accuracy"],
        "system_stage": (
            "institutional_intelligence_ready"
            if timestamp_ready
            and trust["data_trust_index"] >= 90
            else "platform_buildout"
        )
    }
