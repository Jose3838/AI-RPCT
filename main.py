from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.routes import router
from api.auth_routes import router as auth_router
from api.billing_routes import router as billing_router
from api.organization_routes import router as organization_router
from api.forecast_routes import router as forecast_router
from api.provider_routes import router as provider_router
from api.live_data_routes import router as live_data_router
from api.market_routes import router as market_router
from api.enterprise_routes import router as enterprise_router

app = FastAPI(
    title="AI-RPCT",
    version="63.0"
)

app.include_router(router)
app.include_router(auth_router)
app.include_router(billing_router)
app.include_router(organization_router)
app.include_router(forecast_router)
app.include_router(provider_router)
app.include_router(live_data_router)
app.include_router(market_router)
app.include_router(enterprise_router)

app.mount("/web", StaticFiles(directory="web", html=True), name="web")

@app.get("/")
def root():
    return {
        "service": "AI-RPCT",
        "status": "online",
        "version": "63.0",
        "terminal": "/web"
    }

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

from data_layer.executive_intelligence_pipeline import build_dynamic_executive_intelligence_summary

@app.get("/executive-intelligence-summary-v2")
def executive_intelligence_summary_v2():
    return build_dynamic_executive_intelligence_summary()

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

from data_trust_index import build_data_trust_index

@app.get("/data-trust-index")
def data_trust_index():
    return build_data_trust_index()

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

from executive_risk_dashboard import (
    build_executive_risk_dashboard
)

@app.get("/executive-risk-dashboard")
def executive_risk_dashboard():
    return build_executive_risk_dashboard()

