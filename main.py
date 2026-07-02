from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.routes import router
from api.auth_routes import router as auth_router
from api.billing_routes import router as billing_router
from api.organization_routes import router as organization_router
from api.forecast_routes import router as forecast_router

app = FastAPI(
    title="AI-RPCT",
    version="63.0"
)

app.include_router(router)
app.include_router(auth_router)
app.include_router(billing_router)
app.include_router(organization_router)
app.include_router(forecast_router)

app.mount("/web", StaticFiles(directory="web", html=True), name="web")

@app.get("/")
def root():
    return {
        "service": "AI-RPCT",
        "status": "online",
        "version": "63.0",
        "terminal": "/web"
    }

import csv

@app.get("/history-provider-activation")
def history_provider_activation():
    history = []

    try:
        with open("provider_activation_score_history.csv", "r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                history.append({
                    "timestamp": row["timestamp"],
                    "provider": row["provider"],
                    "activation_score": float(row["activation_score"])
                })

    except FileNotFoundError:
        return {
            "status": "missing_history_file",
            "history": []
        }

    return {
        "status": "ok",
        "records": len(history),
        "history": history
    }

from provider_coverage_engine_v3 import get_provider_coverage_v3

@app.get("/provider-coverage-v3")
def provider_coverage_v3():
    return get_provider_coverage_v3()

from provider_activation_score import (
    calculate_provider_activation_score
)

@app.get("/provider-activation-score")
def provider_activation_score():

    providers = [
        {
            "provider": "vast",
            "price_score": 88,
            "capacity_score": 79,
            "health_score": 95,
            "momentum_score": 74
        },
        {
            "provider": "runpod",
            "price_score": 84,
            "capacity_score": 82,
            "health_score": 92,
            "momentum_score": 76
        }
    ]

    results = []

    for provider in providers:

        score = calculate_provider_activation_score(
            provider["price_score"],
            provider["capacity_score"],
            provider["health_score"],
            provider["momentum_score"]
        )

        results.append({
            "provider": provider["provider"],
            **score
        })

    return {
        "providers": results
    }

from market_strength_index import calculate_market_strength_index

@app.get("/market-strength-index")
def market_strength_index():
    provider_scores = [
        85.3,
        84.2
    ]

    return calculate_market_strength_index(provider_scores)

from executive_intelligence_summary import build_executive_intelligence_summary

@app.get("/executive-intelligence-summary")
def executive_intelligence_summary():
    coverage = 33.33
    activation_scores = [
        85.3,
        84.2
    ]
    market_strength = 84.75

    return build_executive_intelligence_summary(
        coverage,
        activation_scores,
        market_strength
    )

from daily_market_snapshot import save_market_snapshot

@app.post("/save-market-snapshot")
def save_market_snapshot_endpoint():

    coverage = 33.33
    market_strength = 84.75
    avg_activation_score = 84.75

    return save_market_snapshot(
        coverage,
        market_strength,
        avg_activation_score
    )

from provider_expansion_tracker import save_provider_expansion

@app.post("/save-provider-expansion")
def save_provider_expansion_endpoint():

    live_providers = 2
    total_providers = 6
    coverage_percentage = 33.33

    return save_provider_expansion(
        live_providers,
        total_providers,
        coverage_percentage
    )

from data_layer.provider_data_pipeline import build_provider_dataset

@app.get("/unified-provider-data")
def unified_provider_data():
    return {
        "status": "ok",
        "records": build_provider_dataset()
    }

from data_layer.provider_scoring_pipeline import build_dynamic_provider_activation_scores

@app.get("/provider-activation-score-v2")
def provider_activation_score_v2():
    return {
        "status": "ok",
        "version": "v2",
        "providers": build_dynamic_provider_activation_scores()
    }

from data_layer.market_strength_pipeline import build_dynamic_market_strength_index

@app.get("/market-strength-index-v2")
def market_strength_index_v2():
    return build_dynamic_market_strength_index()

from data_layer.executive_intelligence_pipeline import build_dynamic_executive_intelligence_summary

@app.get("/executive-intelligence-summary-v2")
def executive_intelligence_summary_v2():
    return build_dynamic_executive_intelligence_summary()

from data_layer.dynamic_snapshot_pipeline import save_dynamic_market_snapshot

@app.post("/save-market-snapshot-v2")
def save_market_snapshot_v2():
    return save_dynamic_market_snapshot()

from data_layer.trend_engine import build_market_trend_summary

@app.get("/market-trend-summary")
def market_trend_summary():
    return build_market_trend_summary()

from weekly_infrastructure_report import build_weekly_infrastructure_report

@app.get("/weekly-infrastructure-report")
def weekly_infrastructure_report():
    return build_weekly_infrastructure_report()

from enterprise_report_index import build_enterprise_report_index

@app.get("/enterprise-report-index")
def enterprise_report_index():
    return build_enterprise_report_index()

from sales_enterprise_bundle import build_sales_enterprise_bundle

@app.get("/sales-enterprise-bundle")
def sales_enterprise_bundle():
    return build_sales_enterprise_bundle()

from enterprise_access import require_enterprise
from sales_enterprise_bundle import build_sales_enterprise_bundle

@app.get("/enterprise-sales-demo")
def enterprise_sales_demo(api_key: str):
    access = require_enterprise(api_key)

    if not access["allowed"]:
        return {
            "status": "blocked",
            **access
        }

    return {
        "status": "ok",
        "access": access,
        "bundle": build_sales_enterprise_bundle()
    }

from providers.connectors.collector import (
    collect_provider_data
)

@app.get("/provider-collector")
def provider_collector():
    return {
        "status": "ok",
        "providers": collect_provider_data()
    }

from provider_expansion_tracker import save_provider_expansion as save_provider_expansion_dynamic

@app.post("/save-provider-expansion-v2")
def save_provider_expansion_v2():
    return save_provider_expansion_dynamic()

from coverage_milestone_report import build_coverage_milestone_report

@app.get("/coverage-milestone-report")
def coverage_milestone_report():
    return build_coverage_milestone_report()

from usage_tracking import track_usage

@app.get("/usage-test")
def usage_test(api_key: str = "demo-free-key"):

    track_usage(
        api_key,
        "/usage-test"
    )

    return {
        "status": "tracked"
    }

from usage_analytics import get_usage_analytics

@app.get("/usage-analytics-v2")
def usage_analytics_v2():
    return {
        "status": "ok",
        "usage": get_usage_analytics()
    }

from dynamic_entitlements import get_plan_for_api_key, require_plan

@app.get("/entitlement-check-v2")
def entitlement_check_v2(api_key: str):
    return {
        "status": "ok",
        "api_key": api_key,
        "plan": get_plan_for_api_key(api_key)
    }


@app.get("/enterprise-check-v2")
def enterprise_check_v2(api_key: str):
    return require_plan(
        api_key,
        ["enterprise"]
    )

from provider_freshness import build_provider_freshness_report
from providers.connectors.collector import collect_provider_data as collect_provider_data_for_freshness

@app.get("/provider-freshness")
def provider_freshness():
    providers = collect_provider_data_for_freshness()
    return build_provider_freshness_report(providers)

from data_trust_index import build_data_trust_index

@app.get("/data-trust-index")
def data_trust_index():
    return build_data_trust_index()

from enterprise_intelligence_bundle_v2 import build_enterprise_intelligence_bundle_v2

@app.get("/enterprise-intelligence-bundle-v2")
def enterprise_intelligence_bundle_v2():
    return build_enterprise_intelligence_bundle_v2()

from dynamic_entitlements import require_plan as require_dynamic_plan
from enterprise_intelligence_bundle_v2 import build_enterprise_intelligence_bundle_v2

@app.get("/enterprise-intelligence-bundle-v2-gated")
def enterprise_intelligence_bundle_v2_gated(api_key: str):
    access = require_dynamic_plan(
        api_key,
        ["enterprise"]
    )

    if not access["allowed"]:
        return {
            "status": "blocked",
            **access
        }

    return {
        "status": "ok",
        "access": access,
        "bundle": build_enterprise_intelligence_bundle_v2()
    }

from automated_snapshot_runner import run_daily_snapshot

@app.post("/run-daily-snapshot")
def run_daily_snapshot_endpoint():
    return run_daily_snapshot()

from historical_query_api import get_historical_data

@app.get("/historical-data")
def historical_data():
    return get_historical_data()

from trend_intelligence import build_trend_intelligence

@app.get("/trend-intelligence")
def trend_intelligence():
    return build_trend_intelligence()

from gpu_scarcity_index import build_gpu_scarcity_index

@app.get("/gpu-scarcity-index")
def gpu_scarcity_index():
    return build_gpu_scarcity_index()

from capacity_pressure_index import build_capacity_pressure_index

@app.get("/capacity-pressure-index")
def capacity_pressure_index():
    return build_capacity_pressure_index()

from infrastructure_risk_signal import build_infrastructure_risk_signal

@app.get("/infrastructure-risk-signal")
def infrastructure_risk_signal():
    return build_infrastructure_risk_signal()

from executive_market_briefing import (
    build_executive_market_briefing
)

@app.get("/executive-market-briefing")
def executive_market_briefing():
    return build_executive_market_briefing()

from historical_intelligence_engine import build_historical_intelligence

@app.get("/historical-intelligence")
def historical_intelligence():
    return build_historical_intelligence()

from provider_ranking_engine import build_provider_ranking

@app.get("/provider-ranking")
def provider_ranking():
    return build_provider_ranking()

from provider_recommendation_engine import build_provider_recommendations

@app.get("/provider-recommendations")
def provider_recommendations():
    return build_provider_recommendations()

from enterprise_decision_engine import build_enterprise_decision_engine

@app.get("/enterprise-decision-engine")
def enterprise_decision_engine():
    return build_enterprise_decision_engine()

from intelligence_registry import build_intelligence_registry

@app.get("/intelligence-registry")
def intelligence_registry():
    return build_intelligence_registry()

from historical_intelligence_v2 import (
    build_historical_intelligence_v2
)

@app.get("/historical-intelligence-v2")
def historical_intelligence_v2():
    return build_historical_intelligence_v2()

from gpu_scarcity_history import (
    save_gpu_scarcity_snapshot,
    load_gpu_scarcity_history
)

@app.post("/save-gpu-scarcity-snapshot")
def save_gpu_scarcity_snapshot_endpoint():
    return save_gpu_scarcity_snapshot()


@app.get("/gpu-scarcity-history")
def gpu_scarcity_history_endpoint():
    return {
        "status": "ok",
        "history": load_gpu_scarcity_history()
    }

from historical_intelligence_score import (
    build_historical_intelligence_score
)

@app.get("/historical-intelligence-score")
def historical_intelligence_score():
    return build_historical_intelligence_score()

from capacity_pressure_history import (
    save_capacity_pressure_snapshot,
    load_capacity_pressure_history
)

@app.post("/save-capacity-pressure-snapshot")
def save_capacity_pressure_snapshot_endpoint():
    return save_capacity_pressure_snapshot()


@app.get("/capacity-pressure-history")
def capacity_pressure_history_endpoint():
    return {
        "status": "ok",
        "history": load_capacity_pressure_history()
    }

from risk_signal_history import (
    save_risk_signal_snapshot,
    load_risk_signal_history
)

@app.post("/save-risk-signal-snapshot")
def save_risk_signal_snapshot_endpoint():
    return save_risk_signal_snapshot()


@app.get("/risk-signal-history")
def risk_signal_history_endpoint():
    return {
        "status": "ok",
        "history": load_risk_signal_history()
    }

from intelligence_quality_dashboard import build_intelligence_quality_dashboard

@app.get("/intelligence-quality-dashboard")
def intelligence_quality_dashboard():
    return build_intelligence_quality_dashboard()

from prediction_research_dashboard import (
    build_prediction_research_dashboard
)

@app.get("/prediction-research-dashboard")
def prediction_research_dashboard():
    return build_prediction_research_dashboard()

from automated_intelligence_snapshot_v2 import run_intelligence_snapshot_v2

@app.post("/run-intelligence-snapshot-v2")
def run_intelligence_snapshot_v2_endpoint():
    return run_intelligence_snapshot_v2()

from data_moat_dashboard import (
    build_data_moat_dashboard
)

@app.get("/data-moat-dashboard")
def data_moat_dashboard():
    return build_data_moat_dashboard()

from intelligence_performance_dashboard import (
    build_intelligence_performance_dashboard
)

@app.get("/intelligence-performance-dashboard")
def intelligence_performance_dashboard():
    return build_intelligence_performance_dashboard()

from data_moat_growth_plan import build_data_moat_growth_plan

@app.get("/data-moat-growth-plan")
def data_moat_growth_plan():
    return build_data_moat_growth_plan()

from history_schema_health import build_history_schema_health

@app.get("/history-schema-health")
def history_schema_health():
    return build_history_schema_health()

from system_readiness_report import build_system_readiness_report

@app.get("/system-readiness-report")
def system_readiness_report():
    return build_system_readiness_report()

from investor_snapshot import build_investor_snapshot

@app.get("/investor-snapshot")
def investor_snapshot():
    return build_investor_snapshot()

from provider_concentration_risk import (
    build_provider_concentration_risk
)

@app.get("/provider-concentration-risk")
def provider_concentration_risk():
    return build_provider_concentration_risk()

from executive_risk_dashboard import (
    build_executive_risk_dashboard
)

@app.get("/executive-risk-dashboard")
def executive_risk_dashboard():
    return build_executive_risk_dashboard()

from connector_health_dashboard import build_connector_health_dashboard

@app.get("/connector-health-dashboard")
def connector_health_dashboard():
    return build_connector_health_dashboard()

from live_data_readiness_score import build_live_data_readiness_score

@app.get("/live-data-readiness-score")
def live_data_readiness_score():
    return build_live_data_readiness_score()

from provider_api_key_readiness import build_provider_api_key_readiness

@app.get("/provider-api-key-readiness")
def provider_api_key_readiness():
    return build_provider_api_key_readiness()

from connector_maturity_dashboard import (
    build_connector_maturity_dashboard
)

@app.get("/connector-maturity-dashboard")
def connector_maturity_dashboard():
    return build_connector_maturity_dashboard()

from connector_coverage_score import build_connector_coverage_score

@app.get("/connector-coverage-score")
def connector_coverage_score():
    return build_connector_coverage_score()

from live_data_migration_plan import build_live_data_migration_plan

@app.get("/live-data-migration-plan")
def live_data_migration_plan():
    return build_live_data_migration_plan()

from live_data_migration_dashboard import build_live_data_migration_dashboard

@app.get("/live-data-migration-dashboard")
def live_data_migration_dashboard():
    return build_live_data_migration_dashboard()

from live_data_quality_v2 import build_live_data_quality_v2

@app.get("/live-data-quality-v2")
def live_data_quality_v2():
    return build_live_data_quality_v2()

from connector_portfolio_score import (
    build_connector_portfolio_score
)

@app.get("/connector-portfolio-score")
def connector_portfolio_score():
    return build_connector_portfolio_score()

from historical_live_data_coverage import (
    build_historical_live_data_coverage
)

@app.get("/historical-live-data-coverage")
def historical_live_data_coverage():
    return build_historical_live_data_coverage()

from live_data_snapshot_auditor import build_live_data_snapshot_audit

@app.get("/live-data-snapshot-audit")
def live_data_snapshot_audit():
    return build_live_data_snapshot_audit()

from live_data_audit_history import (
    save_live_data_audit_snapshot,
    load_live_data_audit_history
)

@app.post("/save-live-data-audit-snapshot")
def save_live_data_audit_snapshot_endpoint():
    return save_live_data_audit_snapshot()


@app.get("/live-data-audit-history")
def live_data_audit_history_endpoint():
    return {
        "status": "ok",
        "history": load_live_data_audit_history()
    }
