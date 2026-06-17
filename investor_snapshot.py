from system_readiness_report import build_system_readiness_report
from data_moat_dashboard import build_data_moat_dashboard
from organization_revenue_dashboard import build_organization_revenue_dashboard
from intelligence_performance_dashboard import build_intelligence_performance_dashboard


def build_investor_snapshot():
    readiness = build_system_readiness_report()
    moat = build_data_moat_dashboard()
    revenue = build_organization_revenue_dashboard()
    performance = build_intelligence_performance_dashboard()

    return {
        "status": "ok",
        "version": "v1",
        "product": "AI-RPCT",
        "positioning": "Bloomberg-style AI Infrastructure Intelligence",
        "system_stage": readiness["system_stage"],
        "data_trust_index": readiness["data_trust_index"],
        "forecast_accuracy": readiness["forecast_accuracy"],
        "data_moat_score": moat["data_moat_score"],
        "total_historical_records": moat["total_records"],
        "monthly_recurring_revenue": revenue["monthly_recurring_revenue"],
        "annual_recurring_revenue": revenue["annual_recurring_revenue"],
        "intelligence_quality": {
            "forecast_error_rate": performance["forecast_error_rate"],
            "weighting_strategy": performance["weighting_strategy"]
        },
        "cto_summary": "AI-RPCT has reached institutional intelligence readiness with strong data trust, active historical collection, forecasting validation, and enterprise monetization infrastructure."
    }
