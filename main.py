from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.routes import router
from api.auth_routes import router as auth_router

app = FastAPI(
    title="AI-RPCT",
    version="63.0"
)

app.include_router(router)
app.include_router(auth_router)

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

from intelligence.features.daily_feature_store import append_daily_features
from intelligence.providers.save_provider_market_share import save_provider_market_share
from intelligence.regime.provider_dominance_regime import provider_dominance_regime
from intelligence.regime.save_provider_dominance_history import save_provider_dominance_history
from intelligence.assets.historical_asset_health import historical_asset_health
from intelligence.lifecycle.offer_lifecycle import detect_offer_changes
from intelligence.signals.capacity_churn_index import calculate_capacity_churn


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

from billing_engine import build_billing_summary

@app.get("/billing-summary")
def billing_summary():
    return {
        "status": "ok",
        "billing": build_billing_summary()
    }

from invoice_generator import generate_invoices

@app.get("/invoice-summary")
def invoice_summary():
    return {
        "status": "ok",
        "invoices": generate_invoices()
    }

from revenue_dashboard import build_revenue_dashboard

@app.get("/revenue-dashboard")
def revenue_dashboard():
    return build_revenue_dashboard()

from organizations import create_organization, list_organizations

@app.post("/create-organization")
def create_organization_endpoint(
    name: str,
    plan: str,
    api_key: str
):
    return create_organization(
        name,
        plan,
        api_key
    )


@app.get("/organizations")
def organizations_endpoint():
    return {
        "status": "ok",
        "organizations": list_organizations()
    }

from organization_revenue_dashboard import build_organization_revenue_dashboard

@app.get("/organization-revenue-dashboard")
def organization_revenue_dashboard():
    return build_organization_revenue_dashboard()

from organization_usage_dashboard import build_organization_usage_dashboard

@app.get("/organization-usage-dashboard")
def organization_usage_dashboard():
    return build_organization_usage_dashboard()

from api_key_management import create_api_key, list_api_keys

@app.post("/create-api-key")
def create_api_key_endpoint(
    organization_id: int,
    plan: str
):
    return create_api_key(
        organization_id,
        plan
    )


@app.get("/api-keys")
def api_keys_endpoint():
    return {
        "status": "ok",
        "api_keys": list_api_keys()
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

from forecast_engine_v2 import build_forecast_engine_v2

@app.get("/forecast-engine-v2")
def forecast_engine_v2():
    return build_forecast_engine_v2()

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

from forecast_engine_v3 import build_forecast_engine_v3

@app.get("/forecast-engine-v3")
def forecast_engine_v3():
    return build_forecast_engine_v3()

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

from forecast_history import (
    save_forecast_snapshot,
    load_forecast_history
)

@app.post("/save-forecast-snapshot")
def save_forecast_snapshot_endpoint():
    return save_forecast_snapshot()


@app.get("/forecast-history")
def forecast_history_endpoint():
    return {
        "status": "ok",
        "history": load_forecast_history()
    }

from forecast_accuracy_engine import (
    build_forecast_accuracy
)

@app.get("/forecast-accuracy")
def forecast_accuracy():
    return build_forecast_accuracy()

from forecast_accuracy_engine import (
    build_forecast_accuracy
)

@app.get("/forecast-accuracy")
def forecast_accuracy():
    return build_forecast_accuracy()

from forecast_validation_engine import (
    build_forecast_validation
)

@app.get("/forecast-validation")
def forecast_validation():
    return build_forecast_validation()

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

from forecast_accuracy_v2 import build_forecast_accuracy_v2

@app.get("/forecast-accuracy-v2")
def forecast_accuracy_v2():
    return build_forecast_accuracy_v2()

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

from forecast_error_tracking import build_forecast_error_tracking

@app.get("/forecast-error-tracking")
def forecast_error_tracking():
    return build_forecast_error_tracking()

from forecast_model_improvement_plan import build_forecast_model_improvement_plan

@app.get("/forecast-model-improvement-plan")
def forecast_model_improvement_plan():
    return build_forecast_model_improvement_plan()

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

from forecast_weight_optimization import build_forecast_weight_optimization

@app.get("/forecast-weight-optimization")
def forecast_weight_optimization():
    return build_forecast_weight_optimization()

from forecast_weight_optimization import build_forecast_weight_optimization

@app.get("/forecast-weight-optimization")
def forecast_weight_optimization():
    return build_forecast_weight_optimization()

from forecast_engine_v31 import build_forecast_engine_v31

@app.get("/forecast-engine-v31")
def forecast_engine_v31():
    return build_forecast_engine_v31()

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

from provider_stability_score import (
    build_provider_stability_score
)

@app.get("/provider-stability-score")
def provider_stability_score():
    return build_provider_stability_score()

from provider_market_leadership import (
    build_provider_market_leadership
)

@app.get("/provider-market-leadership")
def provider_market_leadership():
    return build_provider_market_leadership()

from provider_momentum import build_provider_momentum

@app.get("/provider-momentum")
def provider_momentum():
    return build_provider_momentum()

from provider_momentum_history import (
    save_provider_momentum_snapshot,
    load_provider_momentum_history
)

@app.post("/save-provider-momentum-snapshot")
def save_provider_momentum_snapshot_endpoint():
    return save_provider_momentum_snapshot()


@app.get("/provider-momentum-history")
def provider_momentum_history_endpoint():
    return {
        "status": "ok",
        "history": load_provider_momentum_history()
    }

from automated_intelligence_snapshot_v3 import run_intelligence_snapshot_v3

@app.post("/run-intelligence-snapshot-v3")
def run_intelligence_snapshot_v3_endpoint():
    return run_intelligence_snapshot_v3()

from intelligence_core_v4 import (
    market_regime,
    provider_strength,
    early_warning,
    market_signal,
    snapshot_v4,
)

@app.get("/market-regime-v4")
def market_regime_v4():
    return market_regime()

@app.get("/provider-strength-v4")
def provider_strength_v4():
    return provider_strength()

@app.get("/early-warning-v4")
def early_warning_v4():
    return early_warning()

@app.get("/market-signal-v4")
def market_signal_v4():
    return market_signal()

@app.get("/run-intelligence-snapshot-v4")
def run_intelligence_snapshot_v4():
    return snapshot_v4()

import csv
from pathlib import Path

@app.post("/save-intelligence-snapshot-v4")
def save_intelligence_snapshot_v4():
    snapshot = snapshot_v4()
    file = Path("intelligence_snapshot_v4_history.csv")
    exists = file.exists()

    with file.open("a", newline="") as f:
        writer = csv.writer(f)

        if not exists:
            writer.writerow([
                "timestamp",
                "market_regime",
                "market_signal_score",
                "market_direction",
                "top_provider",
                "weakest_provider"
            ])

        providers = snapshot["provider_strength"]

        writer.writerow([
            snapshot["generated_at"],
            snapshot["market_regime"]["market_regime"],
            snapshot["market_signal"]["market_signal_score"],
            snapshot["market_signal"]["market_direction"],
            providers[0]["provider"] if providers else None,
            providers[-1]["provider"] if providers else None
        ])

    return {
        "status": "saved",
        "file": "intelligence_snapshot_v4_history.csv",
        "snapshot": snapshot
    }

@app.get("/market-signal-trend")
def market_signal_trend():
    import csv
    from pathlib import Path

    file = Path("intelligence_snapshot_v4_history.csv")

    if not file.exists():
        return {"error": "history file not found"}

    with file.open() as f:
        rows = list(csv.DictReader(f))

    if len(rows) < 2:
        return {
            "trend": "insufficient_data",
            "snapshots": len(rows)
        }

    latest = float(rows[-1]["market_signal_score"])
    previous = float(rows[-2]["market_signal_score"])

    delta = round(latest - previous, 2)

    if delta > 0:
        trend = "improving"
    elif delta < 0:
        trend = "deteriorating"
    else:
        trend = "stable"

    return {
        "trend": trend,
        "latest_score": latest,
        "previous_score": previous,
        "delta": delta,
        "snapshots": len(rows)
    }


@app.get("/provider-momentum-trend")
def provider_momentum_trend():

    import csv

    providers = {}

    with open("provider_momentum_history.csv") as f:
        reader = csv.reader(f)

        for row in reader:

            try:
                provider = row[1]
                score = float(row[2])

                providers.setdefault(provider, []).append(score)

            except:
                pass

    result = []

    for provider, scores in providers.items():

        if len(scores) < 2:
            continue

        latest = scores[-1]
        previous = scores[-2]

        delta = round(latest - previous, 2)

        if delta > 0:
            trend = "improving"
        elif delta < 0:
            trend = "declining"
        else:
            trend = "stable"

        result.append({
            "provider": provider,
            "latest_score": latest,
            "previous_score": previous,
            "delta": delta,
            "trend": trend
        })

    return sorted(
        result,
        key=lambda x: x["delta"],
        reverse=True
    )


@app.get("/provider-momentum-leaders")
def provider_momentum_leaders():

    trends = provider_momentum_trend()

    winners = [p for p in trends if p["delta"] > 0]
    losers = [p for p in trends if p["delta"] < 0]
    stable = [p for p in trends if p["delta"] == 0]

    top_winner = winners[0] if winners else None
    top_loser = losers[-1] if losers else None

    return {
        "top_winner": top_winner,
        "top_loser": top_loser,
        "winners": winners,
        "losers": losers,
        "stable": stable,
        "summary": {
            "winner_count": len(winners),
            "loser_count": len(losers),
            "stable_count": len(stable),
            "total_providers": len(trends)
        }
    }


@app.get("/market-rotation-signal")
def market_rotation_signal():

    leaders = provider_momentum_leaders()

    winners = leaders["summary"]["winner_count"]
    losers = leaders["summary"]["loser_count"]
    stable = leaders["summary"]["stable_count"]
    total = leaders["summary"]["total_providers"]

    if total == 0:
        return {"error": "no provider momentum data"}

    winner_ratio = round(winners / total, 2)
    loser_ratio = round(losers / total, 2)
    stable_ratio = round(stable / total, 2)

    if winner_ratio >= 0.6:
        rotation = "broad_positive_rotation"
    elif loser_ratio >= 0.6:
        rotation = "broad_negative_rotation"
    elif winners > 0 and losers > 0:
        rotation = "mixed_rotation"
    else:
        rotation = "flat_rotation"

    return {
        "rotation_signal": rotation,
        "winner_ratio": winner_ratio,
        "loser_ratio": loser_ratio,
        "stable_ratio": stable_ratio,
        "top_winner": leaders["top_winner"],
        "top_loser": leaders["top_loser"],
        "summary": leaders["summary"]
    }


@app.get("/market-intelligence-summary")
def market_intelligence_summary():

    snapshot = snapshot_v4()
    trend = market_signal_trend()
    rotation = market_rotation_signal()
    leaders = provider_momentum_leaders()

    market_regime = snapshot["market_regime"]["market_regime"]
    market_direction = snapshot["market_signal"]["market_direction"]
    signal_score = snapshot["market_signal"]["market_signal_score"]

    top_provider = None
    weakest_provider = None

    if snapshot["provider_strength"]:
        top_provider = snapshot["provider_strength"][0]["provider"]
        weakest_provider = snapshot["provider_strength"][-1]["provider"]

    summary = (
        f"AI-RPCT detects a {market_regime} with {market_direction} market conditions. "
        f"The current market signal score is {signal_score}. "
        f"Momentum trend is {trend['trend']} with delta {trend.get('delta')}. "
        f"Market rotation is {rotation['rotation_signal']}. "
        f"Top provider is {top_provider}; weakest provider is {weakest_provider}."
    )

    return {
        "summary": summary,
        "market_regime": market_regime,
        "market_direction": market_direction,
        "market_signal_score": signal_score,
        "market_signal_trend": trend,
        "market_rotation": rotation,
        "momentum_leaders": leaders
    }


@app.get("/executive-intelligence-brief")
def executive_intelligence_brief():

    summary = market_intelligence_summary()
    snapshot = snapshot_v4()
    rotation = market_rotation_signal()
    leaders = provider_momentum_leaders()

    top_provider = snapshot["provider_strength"][0]["provider"] if snapshot["provider_strength"] else None
    weakest_provider = snapshot["provider_strength"][-1]["provider"] if snapshot["provider_strength"] else None

    risk_level = "low"

    if weakest_provider and rotation["rotation_signal"] == "broad_negative_rotation":
        risk_level = "high"
    elif rotation["rotation_signal"] in ["mixed_rotation", "flat_rotation"]:
        risk_level = "moderate"

    brief = {
        "headline": f"GPU infrastructure market currently shows {summary['market_direction']} conditions.",
        "executive_summary": summary["summary"],
        "key_takeaways": [
            f"Market regime is classified as {summary['market_regime']}.",
            f"Current market signal score is {summary['market_signal_score']}.",
            f"Provider momentum rotation is {rotation['rotation_signal']}.",
            f"Top provider by strength is {top_provider}.",
            f"Weakest provider by strength is {weakest_provider}."
        ],
        "risk_level": risk_level,
        "watchlist": {
            "top_winner": leaders["top_winner"],
            "top_loser": leaders["top_loser"],
            "weakest_provider": weakest_provider
        },
        "recommended_action": (
            "Monitor provider momentum and market signal trend before making capacity allocation decisions."
        ),
        "system_stage": "institutional_market_intelligence"
    }

    return brief


@app.post("/save-executive-intelligence-brief")
def save_executive_intelligence_brief():

    import csv
    from pathlib import Path
    from datetime import datetime

    brief = executive_intelligence_brief()
    file = Path("executive_intelligence_brief_history.csv")
    exists = file.exists()

    with file.open("a", newline="") as f:
        writer = csv.writer(f)

        if not exists:
            writer.writerow([
                "timestamp",
                "headline",
                "risk_level",
                "recommended_action"
            ])

        writer.writerow([
            datetime.utcnow().isoformat(),
            brief["headline"],
            brief["risk_level"],
            brief["recommended_action"]
        ])

    return {
        "status": "saved",
        "file": "executive_intelligence_brief_history.csv",
        "brief": brief
    }


@app.get("/intelligence-accuracy-score")
def intelligence_accuracy_score():

    import csv
    from pathlib import Path

    file = Path("intelligence_snapshot_v4_history.csv")

    if not file.exists():
        return {"accuracy_score": 0}

    with file.open() as f:
        rows = list(csv.DictReader(f))

    total = len(rows)

    if total < 2:
        return {
            "accuracy_score": 100,
            "observations": total
        }

    stable_periods = 0

    for i in range(1, total):

        current = rows[i]["market_direction"]
        previous = rows[i-1]["market_direction"]

        if current == previous:
            stable_periods += 1

    accuracy = round(
        (stable_periods / (total - 1)) * 100,
        2
    )

    return {
        "accuracy_score": accuracy,
        "observations": total,
        "stable_periods": stable_periods
    }


@app.get("/intelligence-confidence-score")
def intelligence_confidence_score():

    snapshot = snapshot_v4()
    accuracy = intelligence_accuracy_score()
    trend = market_signal_trend()

    provider_count = len(snapshot["provider_strength"])
    accuracy_score = accuracy.get("accuracy_score", 0)
    snapshots = accuracy.get("observations", 0)

    data_depth_score = min(100, snapshots * 10)
    provider_coverage_score = min(100, provider_count * 15)

    if trend["trend"] == "stable":
        trend_reliability_score = 90
    elif trend["trend"] in ["improving", "deteriorating"]:
        trend_reliability_score = 70
    else:
        trend_reliability_score = 50

    confidence_score = round(
        (accuracy_score * 0.4)
        + (data_depth_score * 0.25)
        + (provider_coverage_score * 0.25)
        + (trend_reliability_score * 0.10),
        2
    )

    if confidence_score >= 85:
        confidence_level = "high"
    elif confidence_score >= 65:
        confidence_level = "medium"
    else:
        confidence_level = "early_stage"

    return {
        "confidence_score": confidence_score,
        "confidence_level": confidence_level,
        "drivers": {
            "accuracy_score": accuracy_score,
            "data_depth_score": data_depth_score,
            "provider_coverage_score": provider_coverage_score,
            "trend_reliability_score": trend_reliability_score
        },
        "observations": snapshots,
        "provider_count": provider_count
    }


@app.get("/institutional-readiness-score")
def institutional_readiness_score():

    confidence = intelligence_confidence_score()
    accuracy = intelligence_accuracy_score()
    snapshot = snapshot_v4()

    provider_count = len(snapshot["provider_strength"])
    confidence_score = confidence["confidence_score"]
    accuracy_score = accuracy["accuracy_score"]

    live_data_score = min(100, provider_count * 15)

    readiness_score = round(
        (confidence_score * 0.35)
        + (accuracy_score * 0.30)
        + (live_data_score * 0.25)
        + (100 * 0.10),
        2
    )

    if readiness_score >= 85:
        readiness_level = "institutional_ready"
    elif readiness_score >= 70:
        readiness_level = "enterprise_ready"
    elif readiness_score >= 50:
        readiness_level = "investor_preview_ready"
    else:
        readiness_level = "early_stage"

    return {
        "readiness_score": readiness_score,
        "readiness_level": readiness_level,
        "drivers": {
            "confidence_score": confidence_score,
            "accuracy_score": accuracy_score,
            "live_data_score": live_data_score,
            "product_completion_score": 100
        },
        "provider_count": provider_count,
        "system_stage": "gpu_market_intelligence_platform"
    }


@app.get("/provider-alpha-signal")
def provider_alpha_signal():

    snapshot = snapshot_v4()

    providers = snapshot["provider_strength"]

    if not providers:
        return {"error": "no provider data"}

    avg_strength = (
        sum(p["strength_score"] for p in providers)
        / len(providers)
    )

    alpha_providers = []

    for p in providers:

        alpha = round(
            p["strength_score"] - avg_strength,
            2
        )

        if alpha > 0:
            signal = "outperform"
        elif alpha < 0:
            signal = "underperform"
        else:
            signal = "neutral"

        alpha_providers.append({
            "provider": p["provider"],
            "strength_score": p["strength_score"],
            "alpha_score": alpha,
            "signal": signal
        })

    return sorted(
        alpha_providers,
        key=lambda x: x["alpha_score"],
        reverse=True
    )


@app.get("/provider-allocation-signal")
def provider_allocation_signal():

    alpha = provider_alpha_signal()
    warnings = early_warning()

    warning_map = {
        w["provider"]: w["warning_level"]
        for w in warnings
    }

    result = []

    for p in alpha:

        warning = warning_map.get(p["provider"], "unknown")

        if p["signal"] == "outperform" and warning == "normal":
            allocation = "prefer"
        elif p["signal"] == "outperform" and warning in ["watch", "critical"]:
            allocation = "monitor"
        elif p["signal"] == "neutral":
            allocation = "neutral"
        else:
            allocation = "avoid"

        result.append({
            "provider": p["provider"],
            "allocation_signal": allocation,
            "alpha_score": p["alpha_score"],
            "strength_score": p["strength_score"],
            "warning_level": warning
        })

    return sorted(
        result,
        key=lambda x: x["alpha_score"],
        reverse=True
    )


@app.get("/provider-allocation-brief")
def provider_allocation_brief():

    allocation = provider_allocation_signal()

    prefer = [p for p in allocation if p["allocation_signal"] == "prefer"]
    monitor = [p for p in allocation if p["allocation_signal"] == "monitor"]
    avoid = [p for p in allocation if p["allocation_signal"] == "avoid"]
    neutral = [p for p in allocation if p["allocation_signal"] == "neutral"]

    brief = {
        "headline": "AI-RPCT provider allocation model generated current GPU infrastructure recommendations.",
        "preferred_providers": prefer,
        "monitor_providers": monitor,
        "avoid_providers": avoid,
        "neutral_providers": neutral,
        "summary": {
            "prefer_count": len(prefer),
            "monitor_count": len(monitor),
            "avoid_count": len(avoid),
            "neutral_count": len(neutral),
            "total_providers": len(allocation)
        },
        "recommended_action": (
            "Prioritize providers marked as prefer, monitor providers with elevated warnings, "
            "and avoid providers showing underperformance or critical weakness."
        )
    }

    return brief


@app.get("/provider-dominance-index")
def provider_dominance_index():

    providers = provider_strength()

    if not providers:
        return []

    total_strength = sum(
        p["strength_score"]
        for p in providers
    )

    result = []

    for p in providers:

        dominance = round(
            (p["strength_score"] / total_strength) * 100,
            2
        )

        if dominance >= 25:
            tier = "market_leader"
        elif dominance >= 15:
            tier = "major_player"
        elif dominance >= 8:
            tier = "competitive_player"
        else:
            tier = "emerging_player"

        result.append({
            "provider": p["provider"],
            "dominance_index": dominance,
            "tier": tier,
            "strength_score": p["strength_score"]
        })

    return sorted(
        result,
        key=lambda x: x["dominance_index"],
        reverse=True
    )


@app.post("/save-provider-dominance-history")
def save_provider_dominance_history():

    import csv
    from pathlib import Path
    from datetime import datetime

    dominance = provider_dominance_index()

    file = Path("provider_dominance_history.csv")
    exists = file.exists()

    with file.open("a", newline="") as f:

        writer = csv.writer(f)

        if not exists:
            writer.writerow([
                "timestamp",
                "provider",
                "dominance_index",
                "tier"
            ])

        for row in dominance:
            writer.writerow([
                datetime.utcnow().isoformat(),
                row["provider"],
                row["dominance_index"],
                row["tier"]
            ])

    return {
        "status": "saved",
        "providers_saved": len(dominance)
    }


@app.post("/save-provider-dominance-history")
def save_provider_dominance_history():

    import csv
    from pathlib import Path
    from datetime import datetime

    dominance = provider_dominance_index()

    file = Path("provider_dominance_history.csv")
    exists = file.exists()

    with file.open("a", newline="") as f:

        writer = csv.writer(f)

        if not exists:
            writer.writerow([
                "timestamp",
                "provider",
                "dominance_index",
                "tier"
            ])

        for row in dominance:

            writer.writerow([
                datetime.utcnow().isoformat(),
                row["provider"],
                row["dominance_index"],
                row["tier"]
            ])

    return {
        "status": "saved",
        "providers_saved": len(dominance)
    }


@app.get("/provider-dominance-trend")
def provider_dominance_trend():

    import csv
    from pathlib import Path

    file = Path("provider_dominance_history.csv")

    if not file.exists():
        return {"error": "provider dominance history not found"}

    provider_rows = {}

    with file.open() as f:
        reader = csv.DictReader(f)

        for row in reader:
            provider = row["provider"]
            dominance = float(row["dominance_index"])
            provider_rows.setdefault(provider, []).append(dominance)

    result = []

    for provider, values in provider_rows.items():

        if len(values) < 2:
            trend = "insufficient_data"
            delta = 0
            latest = values[-1]
            previous = None
        else:
            latest = values[-1]
            previous = values[-2]
            delta = round(latest - previous, 2)

            if delta > 0:
                trend = "gaining_dominance"
            elif delta < 0:
                trend = "losing_dominance"
            else:
                trend = "stable"

        result.append({
            "provider": provider,
            "latest_dominance": latest,
            "previous_dominance": previous,
            "delta": delta,
            "trend": trend
        })

    return sorted(result, key=lambda x: x["delta"], reverse=True)


@app.get("/dominance-change-alert")
def dominance_change_alert():

    trends = provider_dominance_trend()

    alerts = []

    for p in trends:

        delta = p["delta"]

        if delta >= 5:
            alert = "major_gain"
        elif delta >= 2:
            alert = "moderate_gain"
        elif delta <= -5:
            alert = "major_loss"
        elif delta <= -2:
            alert = "moderate_loss"
        else:
            alert = "no_material_change"

        alerts.append({
            "provider": p["provider"],
            "alert": alert,
            "delta": delta,
            "latest_dominance": p["latest_dominance"],
            "previous_dominance": p["previous_dominance"]
        })

    return alerts


@app.get("/intelligence-master-snapshot")
def intelligence_master_snapshot():

    return {
        "snapshot_v4": snapshot_v4(),
        "market_signal_trend": market_signal_trend(),
        "provider_momentum_trend": provider_momentum_trend(),
        "provider_momentum_leaders": provider_momentum_leaders(),
        "market_rotation_signal": market_rotation_signal(),
        "provider_alpha_signal": provider_alpha_signal(),
        "provider_allocation_signal": provider_allocation_signal(),
        "provider_dominance_index": provider_dominance_index(),
        "provider_dominance_trend": provider_dominance_trend(),
        "dominance_change_alert": dominance_change_alert(),
        "intelligence_confidence": intelligence_confidence_score(),
        "institutional_readiness": institutional_readiness_score(),
        "executive_brief": executive_intelligence_brief()
    }


@app.post("/save-market-regime-history")
def save_market_regime_history():

    import csv
    from pathlib import Path
    from datetime import datetime

    regime = market_regime()

    file = Path("market_regime_history.csv")
    exists = file.exists()

    with file.open("a", newline="") as f:

        writer = csv.writer(f)

        if not exists:
            writer.writerow([
                "timestamp",
                "market_regime",
                "average_provider_momentum"
            ])

        writer.writerow([
            datetime.utcnow().isoformat(),
            regime["market_regime"],
            regime["average_provider_momentum"]
        ])

    return {
        "status": "saved",
        "market_regime": regime["market_regime"]
    }


@app.post("/run-daily-intelligence-cycle")
def run_daily_intelligence_cycle():

    snapshot = save_intelligence_snapshot_v4()
    dominance = save_provider_dominance_history()
    brief = save_executive_intelligence_brief()
    regime = save_market_regime_history()

    return {
        "status": "completed",
        "snapshot": snapshot["status"],
        "dominance": dominance["status"],
        "brief": brief["status"],
        "regime": regime["status"]
    }


@app.get("/intelligence-audit-log")
def intelligence_audit_log():

    from pathlib import Path

    files = [
        "intelligence_snapshot_v4_history.csv",
        "provider_dominance_history.csv",
        "market_regime_history.csv",
        "executive_intelligence_brief_history.csv"
    ]

    audit = []

    for file_name in files:

        path = Path(file_name)

        if path.exists():
            audit.append({
                "file": file_name,
                "size_bytes": path.stat().st_size,
                "exists": True
            })
        else:
            audit.append({
                "file": file_name,
                "exists": False
            })

    return {
        "audit_status": "active",
        "tracked_assets": audit,
        "tracked_asset_count": len(audit)
    }


@app.get("/intelligence-audit-log")
def intelligence_audit_log():

    from pathlib import Path

    files = [
        "intelligence_snapshot_v4_history.csv",
        "provider_dominance_history.csv",
        "market_regime_history.csv",
        "executive_intelligence_brief_history.csv"
    ]

    audit = []

    for file_name in files:

        path = Path(file_name)

        if path.exists():
            audit.append({
                "file": file_name,
                "size_bytes": path.stat().st_size,
                "exists": True
            })
        else:
            audit.append({
                "file": file_name,
                "exists": False
            })

    return {
        "audit_status": "active",
        "tracked_assets": audit,
        "tracked_asset_count": len(audit)
    }


@app.get("/intelligence-asset-health")
def intelligence_asset_health():

    import csv
    from pathlib import Path

    files = [
        "intelligence_snapshot_v4_history.csv",
        "provider_dominance_history.csv",
        "market_regime_history.csv",
        "executive_intelligence_brief_history.csv"
    ]

    assets = []

    for file_name in files:

        path = Path(file_name)

        if not path.exists():
            assets.append({
                "file": file_name,
                "status": "missing",
                "rows": 0
            })
            continue

        with path.open() as f:
            rows = list(csv.reader(f))

        data_rows = max(0, len(rows) - 1)

        if data_rows >= 10:
            status = "healthy"
        elif data_rows >= 1:
            status = "early_data"
        else:
            status = "empty"

        assets.append({
            "file": file_name,
            "status": status,
            "rows": data_rows
        })

    healthy_count = len([a for a in assets if a["status"] in ["healthy", "early_data"]])

    return {
        "asset_health_status": "active",
        "healthy_assets": healthy_count,
        "total_assets": len(assets),
        "assets": assets
    }


@app.get("/intelligence-asset-maturity-score")
def intelligence_asset_maturity_score():

    health = intelligence_asset_health()

    assets = health["assets"]

    if not assets:
        return {"maturity_score": 0, "maturity_level": "no_assets"}

    score = 0

    for asset in assets:
        rows = asset["rows"]

        if rows >= 100:
            asset_score = 100
        elif rows >= 50:
            asset_score = 75
        elif rows >= 10:
            asset_score = 50
        elif rows >= 1:
            asset_score = 25
        else:
            asset_score = 0

        score += asset_score

    maturity_score = round(score / len(assets), 2)

    if maturity_score >= 80:
        maturity_level = "institutional_data_maturity"
    elif maturity_score >= 50:
        maturity_level = "growing_data_moat"
    elif maturity_score >= 25:
        maturity_level = "early_data_moat"
    else:
        maturity_level = "insufficient_history"

    return {
        "maturity_score": maturity_score,
        "maturity_level": maturity_level,
        "assets_evaluated": len(assets),
        "asset_health": assets
    }


@app.get("/data-moat-score")
def data_moat_score():

    maturity = intelligence_asset_maturity_score()
    health = intelligence_asset_health()
    confidence = intelligence_confidence_score()

    maturity_score = maturity["maturity_score"]
    confidence_score = confidence["confidence_score"]

    asset_coverage_score = round(
        (health["healthy_assets"] / health["total_assets"]) * 100,
        2
    ) if health["total_assets"] else 0

    moat_score = round(
        (maturity_score * 0.4)
        + (confidence_score * 0.35)
        + (asset_coverage_score * 0.25),
        2
    )

    if moat_score >= 80:
        moat_level = "strong_data_moat"
    elif moat_score >= 60:
        moat_level = "growing_data_moat"
    elif moat_score >= 35:
        moat_level = "early_data_moat"
    else:
        moat_level = "weak_data_moat"

    return {
        "data_moat_score": moat_score,
        "data_moat_level": moat_level,
        "drivers": {
            "maturity_score": maturity_score,
            "confidence_score": confidence_score,
            "asset_coverage_score": asset_coverage_score
        },
        "tracked_assets": health["assets"]
    }


@app.get("/intelligence-data-inventory")
def intelligence_data_inventory():

    import csv
    from pathlib import Path

    files = [
        "intelligence_snapshot_v4_history.csv",
        "provider_dominance_history.csv",
        "market_regime_history.csv",
        "executive_intelligence_brief_history.csv",
        "provider_momentum_history.csv"
    ]

    inventory = []
    total_rows = 0

    for file_name in files:

        path = Path(file_name)

        if not path.exists():
            continue

        with path.open() as f:
            rows = list(csv.reader(f))

        row_count = max(0, len(rows) - 1)

        total_rows += row_count

        inventory.append({
            "file": file_name,
            "rows": row_count,
            "size_bytes": path.stat().st_size
        })

    return {
        "total_assets": len(inventory),
        "total_data_points": total_rows,
        "inventory": inventory
    }


@app.get("/daily-intelligence-status")
def daily_intelligence_status():

    inventory = intelligence_data_inventory()
    moat = data_moat_score()
    readiness = institutional_readiness_score()

    return {
        "system_status": "active",
        "data_points": inventory["total_data_points"],
        "tracked_assets": inventory["total_assets"],
        "data_moat_score": moat["data_moat_score"],
        "institutional_readiness": readiness["readiness_level"]
    }


@app.get("/provider-coverage")
def provider_coverage():

    providers = provider_strength()

    return {
        "providers_tracked": len(providers),
        "providers": [
            p["provider"]
            for p in providers
        ]
    }


@app.get("/intelligence-growth")
def intelligence_growth():

    inventory = intelligence_data_inventory()

    total_points = inventory["total_data_points"]

    if total_points >= 10000:
        stage = "institutional_scale"
    elif total_points >= 1000:
        stage = "expanding_moat"
    elif total_points >= 100:
        stage = "building_moat"
    else:
        stage = "early_stage"

    return {
        "total_data_points": total_points,
        "growth_stage": stage,
        "tracked_assets": inventory["total_assets"]
    }


from providers.connectors.collector import (
    collect_provider_data
)

@app.get("/connector-live-readiness")
def connector_live_readiness():

    data = collect_provider_data()

    providers = data["providers"]

    readiness = []

    for p in providers:

        readiness.append({
            "provider": p["provider"],
            "live_ready": p.get("live_ready", False),
            "mode": p.get("mode", "unknown"),
            "reason": p.get("reason", "")
        })

    summary = data["summary"]

    readiness_score = round(
        (summary["live_ready"] /
         summary["total_connectors"]) * 100,
        2
    )

    return {
        "readiness_score": readiness_score,
        "summary": summary,
        "providers": readiness
    }


@app.get("/provider-api-key-readiness-v4")
def provider_api_key_readiness_v4():

    import os

    required_keys = {
        "lambda": "LAMBDA_API_KEY",
        "nebius": "NEBIUS_API_KEY",
        "coreweave": "COREWEAVE_API_KEY",
        "crusoe": "CRUSOE_API_KEY",
        "vast": "VAST_API_KEY",
        "runpod": "RUNPOD_API_KEY"
    }

    providers = []

    ready_count = 0

    for provider, env_key in required_keys.items():

        exists = bool(os.getenv(env_key))

        if exists:
            ready_count += 1

        providers.append({
            "provider": provider,
            "env_key": env_key,
            "api_key_present": exists,
            "status": "ready" if exists else "missing"
        })

    readiness_score = round(
        (ready_count / len(required_keys)) * 100,
        2
    )

    return {
        "api_key_readiness_score": readiness_score,
        "ready_count": ready_count,
        "total_required": len(required_keys),
        "providers": providers
    }


@app.get("/connector-mode-summary-v4")
def connector_mode_summary_v4():

    data = collect_provider_data()
    providers = data["providers"]

    live = []
    demo = []
    live_ready = []

    for p in providers:
        item = {
            "provider": p["provider"],
            "mode": p.get("mode", "unknown"),
            "live_ready": p.get("live_ready", False),
            "reason": p.get("reason", "")
        }

        if p.get("mode") == "live":
            live.append(item)
        elif p.get("live_ready"):
            live_ready.append(item)
        else:
            demo.append(item)

    return {
        "live_count": len(live),
        "live_ready_count": len(live_ready),
        "demo_count": len(demo),
        "total": len(providers),
        "live": live,
        "live_ready": live_ready,
        "demo": demo
    }


@app.get("/live-coverage-score-v4")
def live_coverage_score_v4():

    summary = connector_mode_summary_v4()
    total = summary["total"]

    if total == 0:
        return {"live_coverage_score": 0}

    score = round(
        ((summary["live_count"] + summary["live_ready_count"] * 0.5) / total) * 100,
        2
    )

    return {
        "live_coverage_score": score,
        "live_count": summary["live_count"],
        "live_ready_count": summary["live_ready_count"],
        "demo_count": summary["demo_count"],
        "total_connectors": total
    }


@app.post("/save-connector-readiness-audit")
def save_connector_readiness_audit():

    import csv
    from pathlib import Path
    from datetime import datetime

    coverage = live_coverage_score_v4()
    summary = connector_mode_summary_v4()

    file = Path("connector_readiness_audit_history.csv")
    exists = file.exists()

    with file.open("a", newline="") as f:
        writer = csv.writer(f)

        if not exists:
            writer.writerow([
                "timestamp",
                "live_coverage_score",
                "live_count",
                "live_ready_count",
                "demo_count",
                "total_connectors"
            ])

        writer.writerow([
            datetime.utcnow().isoformat(),
            coverage["live_coverage_score"],
            coverage["live_count"],
            coverage["live_ready_count"],
            coverage["demo_count"],
            coverage["total_connectors"]
        ])

    return {
        "status": "saved",
        "file": "connector_readiness_audit_history.csv",
        "coverage": coverage,
        "summary": summary
    }


@app.get("/next-live-provider-target")
def next_live_provider_target():

    summary = connector_mode_summary_v4()

    candidates = summary["demo"] + summary["live_ready"]

    priority = ["lambda", "nebius", "coreweave", "crusoe"]

    for target in priority:
        for p in candidates:
            if p["provider"] == target:
                return {
                    "next_target": target,
                    "reason": p.get("reason", ""),
                    "recommended_action": f"Add real API fetch implementation and API key for {target}."
                }

    return {
        "next_target": None,
        "recommended_action": "All priority providers are already live or no target found."
    }


@app.get("/live-connector-status-v4")
def live_connector_status_v4():

    data = collect_provider_data()

    return {
        "system": "AI-RPCT",
        "status": "active",
        "connector_summary": data["summary"],
        "providers": [
            {
                "provider": p["provider"],
                "mode": p.get("mode", "unknown"),
                "live_ready": p.get("live_ready", False),
                "reason": p.get("reason", "")
            }
            for p in data["providers"]
        ]
    }


@app.get("/live-provider-upgrade-plan")
def live_provider_upgrade_plan():

    target = next_live_provider_target()

    return {
        "next_provider": target["next_target"],
        "recommended_action": target["recommended_action"],
        "steps": [
            "Add provider API key to local .env",
            "Confirm connector returns live_ready=True",
            "Implement real API fetch",
            "Normalize response into AI-RPCT provider schema",
            "Save live data into historical CSV",
            "Recalculate live coverage score"
        ]
    }


@app.get("/environment-readiness-v4")
def environment_readiness_v4():

    import os
    from pathlib import Path

    env_file_exists = Path(".env").exists()

    keys = [
        "LAMBDA_API_KEY",
        "NEBIUS_API_KEY",
        "COREWEAVE_API_KEY",
        "CRUSOE_API_KEY",
        "VAST_API_KEY",
        "RUNPOD_API_KEY"
    ]

    present = []
    missing = []

    for key in keys:
        if os.getenv(key):
            present.append(key)
        else:
            missing.append(key)

    return {
        "env_file_exists": env_file_exists,
        "present_keys_count": len(present),
        "missing_keys_count": len(missing),
        "present_keys": present,
        "missing_keys": missing
    }


@app.post("/run-daily-connector-cycle")
def run_daily_connector_cycle():

    status = live_connector_status_v4()
    api_keys = provider_api_key_readiness_v4()
    coverage = live_coverage_score_v4()
    audit = save_connector_readiness_audit()
    next_target = next_live_provider_target()
    environment = environment_readiness_v4()

    return {
        "status": "completed",
        "connector_status": status,
        "api_key_readiness": api_keys,
        "live_coverage": coverage,
        "audit_saved": audit["status"],
        "next_live_provider_target": next_target,
        "environment": environment
    }


@app.post("/run-master-daily-cycle")
def run_master_daily_cycle():

    intelligence = run_daily_intelligence_cycle()
    connectors = run_daily_connector_cycle()
    moat = data_moat_score()
    readiness = institutional_readiness_score()
    inventory = intelligence_data_inventory()

    return {
        "status": "completed",
        "system": "AI-RPCT",
        "cycle": "master_daily_cycle",
        "intelligence_cycle": intelligence,
        "connector_cycle": connectors,
        "data_moat": moat,
        "institutional_readiness": readiness,
        "data_inventory": inventory
    }


@app.get("/cycle-health-v4")
def cycle_health_v4():

    import csv
    from pathlib import Path

    files = {
        "intelligence_snapshot": "intelligence_snapshot_v4_history.csv",
        "connector_readiness": "connector_readiness_audit_history.csv",
        "market_regime": "market_regime_history.csv",
        "provider_dominance": "provider_dominance_history.csv",
        "executive_brief": "executive_intelligence_brief_history.csv"
    }

    health = {}

    for name, file_name in files.items():

        path = Path(file_name)

        if not path.exists():
            health[name] = {
                "exists": False,
                "rows": 0,
                "status": "missing"
            }
            continue

        with path.open() as f:
            rows = list(csv.reader(f))

        data_rows = max(0, len(rows) - 1)

        if data_rows >= 1:
            status = "active"
        else:
            status = "empty"

        health[name] = {
            "exists": True,
            "rows": data_rows,
            "status": status
        }

    active_count = len([
        h for h in health.values()
        if h["status"] == "active"
    ])

    return {
        "cycle_health": "healthy" if active_count == len(files) else "incomplete",
        "active_assets": active_count,
        "total_assets": len(files),
        "assets": health
    }


@app.post("/save-master-cycle-summary")
def save_master_cycle_summary():

    import csv
    from pathlib import Path
    from datetime import datetime

    moat = data_moat_score()
    readiness = institutional_readiness_score()
    coverage = live_coverage_score_v4()
    inventory = intelligence_data_inventory()
    health = cycle_health_v4()

    file = Path("master_cycle_summary_history.csv")
    exists = file.exists()

    with file.open("a", newline="") as f:
        writer = csv.writer(f)

        if not exists:
            writer.writerow([
                "timestamp",
                "data_moat_score",
                "data_moat_level",
                "readiness_score",
                "readiness_level",
                "live_coverage_score",
                "total_data_points",
                "cycle_health"
            ])

        writer.writerow([
            datetime.utcnow().isoformat(),
            moat["data_moat_score"],
            moat["data_moat_level"],
            readiness["readiness_score"],
            readiness["readiness_level"],
            coverage["live_coverage_score"],
            inventory["total_data_points"],
            health["cycle_health"]
        ])

    return {
        "status": "saved",
        "file": "master_cycle_summary_history.csv"
    }


@app.post("/run-master-daily-cycle-v2")
def run_master_daily_cycle_v2():

    master = run_master_daily_cycle()
    summary = save_master_cycle_summary()
    health = cycle_health_v4()

    feature_snapshot = append_daily_features()
    lifecycle = detect_offer_changes()
    capacity_churn = calculate_capacity_churn()
    provider_market_share = save_provider_market_share()
    provider_dominance = provider_dominance_regime()
    provider_dominance_history = save_provider_dominance_history()
    historical_assets = historical_asset_health()

    return {
        "status": "completed",
        "system": "AI-RPCT",
        "cycle": "master_daily_cycle_v2",
        "master_cycle": master,
        "summary_saved": summary["status"],
        "cycle_health": health,
        "feature_snapshot": feature_snapshot,
        "lifecycle": lifecycle,
        "capacity_churn": capacity_churn,
        "provider_market_share": provider_market_share,
        "provider_dominance": provider_dominance,
        "provider_dominance_history": provider_dominance_history,
        "historical_assets": historical_assets
    }


@app.get("/master-cycle-report")
def master_cycle_report():

    import csv
    from pathlib import Path

    file = Path("master_cycle_summary_history.csv")

    if not file.exists():
        return {"error": "master cycle summary history not found"}

    with file.open() as f:
        rows = list(csv.DictReader(f))

    if not rows:
        return {"error": "no master cycle summaries found"}

    latest = rows[-1]

    report = (
        f"AI-RPCT master cycle is {latest['cycle_health']}. "
        f"Data moat score is {latest['data_moat_score']} "
        f"({latest['data_moat_level']}). "
        f"Institutional readiness is {latest['readiness_level']} "
        f"with score {latest['readiness_score']}. "
        f"Live coverage score is {latest['live_coverage_score']}. "
        f"Total intelligence data points: {latest['total_data_points']}."
    )

    return {
        "report": report,
        "latest": latest,
        "history_points": len(rows)
    }


@app.get("/master-cycle-trend")
def master_cycle_trend():

    import csv
    from pathlib import Path

    file = Path("master_cycle_summary_history.csv")

    if not file.exists():
        return {"error": "master cycle summary history not found"}

    with file.open() as f:
        rows = list(csv.DictReader(f))

    if len(rows) < 2:
        return {
            "trend": "insufficient_data",
            "history_points": len(rows)
        }

    latest = rows[-1]
    previous = rows[-2]

    moat_delta = round(
        float(latest["data_moat_score"]) - float(previous["data_moat_score"]),
        2
    )

    readiness_delta = round(
        float(latest["readiness_score"]) - float(previous["readiness_score"]),
        2
    )

    live_coverage_delta = round(
        float(latest["live_coverage_score"]) - float(previous["live_coverage_score"]),
        2
    )

    if moat_delta > 0 or readiness_delta > 0 or live_coverage_delta > 0:
        trend = "improving"
    elif moat_delta < 0 or readiness_delta < 0 or live_coverage_delta < 0:
        trend = "deteriorating"
    else:
        trend = "stable"

    return {
        "trend": trend,
        "history_points": len(rows),
        "deltas": {
            "data_moat_delta": moat_delta,
            "readiness_delta": readiness_delta,
            "live_coverage_delta": live_coverage_delta
        },
        "latest": latest,
        "previous": previous
    }


@app.get("/command-center-v4")
def command_center_v4():

    return {
        "system": "AI-RPCT",
        "stage": "gpu_market_intelligence_command_center",
        "master_report": master_cycle_report(),
        "master_trend": master_cycle_trend(),
        "cycle_health": cycle_health_v4(),
        "live_coverage": live_coverage_score_v4(),
        "next_live_provider": next_live_provider_target(),
        "data_moat": data_moat_score(),
        "institutional_readiness": institutional_readiness_score()
    }


@app.post("/save-command-center-history")
def save_command_center_history():

    import csv
    from pathlib import Path
    from datetime import datetime

    command = command_center_v4()

    file = Path("command_center_history.csv")
    exists = file.exists()

    moat = command["data_moat"]
    readiness = command["institutional_readiness"]
    coverage = command["live_coverage"]
    health = command["cycle_health"]

    with file.open("a", newline="") as f:
        writer = csv.writer(f)

        if not exists:
            writer.writerow([
                "timestamp",
                "data_moat_score",
                "data_moat_level",
                "readiness_score",
                "readiness_level",
                "live_coverage_score",
                "cycle_health"
            ])

        writer.writerow([
            datetime.utcnow().isoformat(),
            moat["data_moat_score"],
            moat["data_moat_level"],
            readiness["readiness_score"],
            readiness["readiness_level"],
            coverage["live_coverage_score"],
            health["cycle_health"]
        ])

    return {
        "status": "saved",
        "file": "command_center_history.csv"
    }


@app.get("/command-center-trend")
def command_center_trend():

    import csv
    from pathlib import Path

    file = Path("command_center_history.csv")

    if not file.exists():
        return {"error": "command center history not found"}

    with file.open() as f:
        rows = list(csv.DictReader(f))

    if len(rows) < 2:
        return {
            "trend": "insufficient_data",
            "history_points": len(rows)
        }

    latest = rows[-1]
    previous = rows[-2]

    moat_delta = round(
        float(latest["data_moat_score"]) - float(previous["data_moat_score"]),
        2
    )

    readiness_delta = round(
        float(latest["readiness_score"]) - float(previous["readiness_score"]),
        2
    )

    coverage_delta = round(
        float(latest["live_coverage_score"]) - float(previous["live_coverage_score"]),
        2
    )

    if moat_delta > 0 or readiness_delta > 0 or coverage_delta > 0:
        trend = "improving"
    elif moat_delta < 0 or readiness_delta < 0 or coverage_delta < 0:
        trend = "deteriorating"
    else:
        trend = "stable"

    return {
        "trend": trend,
        "history_points": len(rows),
        "deltas": {
            "data_moat_delta": moat_delta,
            "readiness_delta": readiness_delta,
            "live_coverage_delta": coverage_delta
        },
        "latest": latest,
        "previous": previous
    }


@app.get("/startup-readiness-check")
def startup_readiness_check():

    command = command_center_v4()
    env = environment_readiness_v4()
    keys = provider_api_key_readiness_v4()
    cycle = cycle_health_v4()
    next_target = next_live_provider_target()

    blockers = []

    if env["missing_keys_count"] > 0:
        blockers.append("missing_provider_api_keys")

    if cycle["cycle_health"] != "healthy":
        blockers.append("incomplete_cycle_assets")

    if command["live_coverage"]["live_coverage_score"] < 50:
        blockers.append("live_coverage_below_50")

    if not blockers:
        status = "ready_for_next_live_provider"
    else:
        status = "not_fully_ready"

    return {
        "status": status,
        "blockers": blockers,
        "missing_keys": env["missing_keys"],
        "api_key_readiness": keys,
        "cycle_health": cycle,
        "next_live_provider": next_target
    }


@app.get("/final-operating-status")
def final_operating_status():

    return {
        "system": "AI-RPCT",
        "operating_status": "active",
        "command_center": command_center_v4(),
        "command_center_trend": command_center_trend(),
        "startup_readiness": startup_readiness_check(),
        "next_action": next_live_provider_target()
    }


@app.get("/terminal-intelligence-summary-v1")
def terminal_intelligence_summary_v1():

    from intelligence.signals.provider_concentration_risk import provider_concentration_risk
    from intelligence.signals.market_breadth_index import market_breadth_index
    from intelligence.assets.asset_growth_tracker import asset_growth_tracker
    from intelligence.assets.snapshot_integrity import snapshot_integrity
    from intelligence.market_depth.gpu_market_depth import gpu_market_depth

    return {
        "status": "ok",
        "provider_concentration": provider_concentration_risk(),
        "market_breadth": market_breadth_index(),
        "asset_growth": asset_growth_tracker(),
        "snapshot_integrity": snapshot_integrity(),
        "gpu_market_depth": gpu_market_depth()[:15],
        "gpu_market_leaders": __import__(
            "intelligence.market_depth.gpu_market_leaders",
            fromlist=["gpu_market_leaders"]
        ).gpu_market_leaders()[:15],
        "daily_alpha_feed": __import__(
            "intelligence.events.daily_alpha_feed",
            fromlist=["daily_alpha_feed"]
        ).daily_alpha_feed()
    }

@app.get("/terminal-market-narrative-v1")
def terminal_market_narrative_v1():

    from intelligence.signals.provider_concentration_risk import provider_concentration_risk
    from intelligence.signals.market_breadth_index import market_breadth_index
    from intelligence.assets.snapshot_integrity import snapshot_integrity

    concentration = provider_concentration_risk()
    breadth = market_breadth_index()
    integrity = snapshot_integrity()

    risk = concentration.get("risk", "unknown")
    share = concentration.get("largest_provider_share", 0)
    rows = integrity.get("rows", 0)
    gpu_models = integrity.get("gpu_models", 0)

    if risk == "high":
        risk_text = "Provider concentration remains high. Market coverage is still heavily dependent on the leading data source."
    elif risk == "medium":
        risk_text = "Provider concentration is moderate. The platform is beginning to diversify its market coverage."
    else:
        risk_text = "Provider concentration is healthy. Market observations are reasonably diversified across providers."

    return {
        "status": "ok",
        "headline": "AI-RPCT is building a historical GPU market intelligence asset.",
        "summary": (
            f"The system currently tracks {rows} historical offer observations "
            f"across {gpu_models} GPU markets. "
            f"The largest provider represents {round(share * 100, 1)}% of observed data. "
            f"{risk_text}"
        ),
        "risk_level": risk,
        "provider_concentration": concentration,
        "market_breadth": breadth,
        "snapshot_integrity": integrity
    }

@app.get("/terminal-investor-snapshot-v1")
def terminal_investor_snapshot_v1():

    from intelligence.assets.snapshot_integrity import snapshot_integrity
    from intelligence.signals.provider_concentration_risk import provider_concentration_risk
    from intelligence.signals.market_breadth_index import market_breadth_index

    integrity = snapshot_integrity()
    concentration = provider_concentration_risk()
    breadth = market_breadth_index()

    rows = integrity.get("rows", 0)
    providers = integrity.get("providers", 0)
    gpu_models = integrity.get("gpu_models", 0)
    risk = concentration.get("risk", "unknown")

    return {
        "status": "ok",
        "positioning": "Bloomberg-style GPU infrastructure intelligence terminal",
        "data_asset": {
            "historical_observations": rows,
            "providers_tracked": providers,
            "gpu_markets_tracked": gpu_models,
            "market_breadth": breadth
        },
        "risk": {
            "provider_concentration": risk,
            "largest_provider_share": concentration.get("largest_provider_share")
        },
        "commercial_readout": (
            f"AI-RPCT currently tracks {rows} historical GPU offer observations "
            f"across {gpu_models} GPU markets and {providers} providers. "
            f"The current commercial risk is provider concentration: {risk}."
        )
    }

@app.get("/terminal-data-moat-v1")
def terminal_data_moat_v1():

    from intelligence.assets.asset_growth_tracker import asset_growth_tracker
    from intelligence.assets.snapshot_integrity import snapshot_integrity

    assets = asset_growth_tracker()
    integrity = snapshot_integrity()

    total_bytes = sum(assets.values())

    return {
        "status": "ok",
        "total_asset_bytes": total_bytes,
        "assets": assets,
        "observations": integrity.get("rows", 0),
        "gpu_models": integrity.get("gpu_models", 0),
        "providers": integrity.get("providers", 0),
        "readout": (
            f"AI-RPCT currently owns {integrity.get('rows', 0)} historical GPU market observations "
            f"across {integrity.get('gpu_models', 0)} GPU markets and {integrity.get('providers', 0)} providers."
        )
    }

@app.get("/terminal-signal-tape-v1")
def terminal_signal_tape_v1():

    from intelligence.signals.provider_concentration_risk import provider_concentration_risk
    from intelligence.assets.snapshot_integrity import snapshot_integrity
    from intelligence.signals.market_breadth_index import market_breadth_index
    from intelligence.assets.asset_growth_tracker import asset_growth_tracker

    concentration = provider_concentration_risk()
    integrity = snapshot_integrity()
    breadth = market_breadth_index()
    assets = asset_growth_tracker()

    total_bytes = sum(assets.values())

    signals = [
        {
            "type": "data_moat",
            "label": f"{integrity.get('rows', 0)} historical observations tracked"
        },
        {
            "type": "market_breadth",
            "label": f"{breadth.get('gpu_markets', 0)} GPU markets tracked"
        },
        {
            "type": "provider_concentration",
            "label": f"Provider concentration risk: {concentration.get('risk', 'unknown')}"
        },
        {
            "type": "asset_growth",
            "label": f"Historical asset size: {round(total_bytes / 1024, 1)} KB"
        }
    ]

    return {
        "status": "ok",
        "signals": signals
    }

@app.get("/terminal-market-movers-v1")
def terminal_market_movers_v1():

    from intelligence.signals.gpu_price_trend import (
        gpu_price_trend
    )

    trends = gpu_price_trend()

    gainers = [
        x for x in trends
        if x["price_change"] > 0
    ][:10]

    losers = [
        x for x in trends
        if x["price_change"] < 0
    ][:10]

    return {
        "gainers": gainers,
        "losers": losers
    }

@app.get("/terminal-market-movers-v1")
def terminal_market_movers_v1():

    from intelligence.signals.gpu_price_trend import (
        gpu_price_trend
    )

    trends = gpu_price_trend()

    gainers = [
        x for x in trends
        if x["price_change"] > 0
    ][:10]

    losers = [
        x for x in trends
        if x["price_change"] < 0
    ][:10]

    return {
        "status": "ok",
        "gainers": gainers,
        "losers": losers
    }

@app.get("/terminal-provider-risk-v1")
def terminal_provider_risk_v1():

    from intelligence.signals.provider_concentration_risk import (
        provider_concentration_risk
    )

    risk = provider_concentration_risk()

    return {
        "status": "ok",
        "risk": risk,
        "headline": f"Provider concentration risk is {risk.get('risk', 'unknown')}",
        "readout": (
            f"Largest provider share is "
            f"{round(risk.get('largest_provider_share', 0) * 100, 1)}%."
        )
    }

@app.get("/terminal-forecast-readiness-v1")
def terminal_forecast_readiness_v1():

    from intelligence.assets.snapshot_integrity import snapshot_integrity
    from intelligence.signals.market_breadth_index import market_breadth_index

    integrity = snapshot_integrity()
    breadth = market_breadth_index()

    rows = integrity.get("rows", 0)
    gpu_models = integrity.get("gpu_models", 0)

    score = 0

    if rows >= 500:
        score += 35
    if rows >= 5000:
        score += 25
    if gpu_models >= 10:
        score += 25
    if breadth.get("gpu_markets", 0) >= 10:
        score += 15

    return {
        "status": "ok",
        "forecast_readiness_score": min(score, 100),
        "rows": rows,
        "gpu_models": gpu_models,
        "readout": (
            f"Forecast readiness is {min(score, 100)}/100 based on "
            f"{rows} observations and {gpu_models} GPU markets."
        )
    }

@app.get("/terminal-system-health-v1")
def terminal_system_health_v1():

    from pathlib import Path
    from intelligence.assets.snapshot_integrity import snapshot_integrity

    integrity = snapshot_integrity()

    files = {
        "offer_history": Path("data/live_offers/provider_live_offer_history.csv").exists(),
        "feature_store": Path("data/feature_store/daily_market_features.csv").exists(),
        "market_depth_history": Path("data/feature_store/gpu_market_depth_history.csv").exists(),
        "runner_log": Path("logs/master_daily_cycle.log").exists()
    }

    healthy = all(files.values())

    return {
        "status": "healthy" if healthy else "incomplete",
        "files": files,
        "daily_runner_health": terminal_daily_runner_health_v1(),
        "collection_health": terminal_collection_health_v2(),
        "rows": integrity.get("rows", 0),
        "providers": integrity.get("providers", 0),
        "gpu_models": integrity.get("gpu_models", 0)
    }

@app.get("/terminal-demo-warning-v1")
def terminal_demo_warning_v1():

    import os

    missing = []

    for key in [
        "LAMBDA_API_KEY",
        "NEBIUS_API_KEY",
        "COREWEAVE_API_KEY",
        "CRUSOE_API_KEY"
    ]:
        if not os.getenv(key):
            missing.append(key)

    return {
        "status": "ok",
        "missing_keys": missing,
        "demo_mode": len(missing) > 0,
        "readout": (
            f"{len(missing)} provider API keys missing. "
            "Some providers may run in demo mode."
        )
    }

@app.get("/terminal-executive-summary-v1")
def terminal_executive_summary_v1():

    from intelligence.assets.snapshot_integrity import (
        snapshot_integrity
    )

    from main import (
        terminal_forecast_readiness_v1
    )

    integrity = snapshot_integrity()
    forecast = terminal_forecast_readiness_v1()

    return {
        "observations":
            integrity.get("rows", 0),

        "providers":
            integrity.get("providers", 0),

        "gpu_models":
            integrity.get("gpu_models", 0),

        "forecast_readiness":
            forecast.get(
                "forecast_readiness_score",
                0
            )
    }

@app.get("/terminal-market-regime-v1")
def terminal_market_regime_v1():

    from intelligence.signals.provider_concentration_risk import (
        provider_concentration_risk
    )
    from intelligence.signals.market_breadth_index import (
        market_breadth_index
    )
    from intelligence.assets.snapshot_integrity import (
        snapshot_integrity
    )

    concentration = provider_concentration_risk()
    breadth = market_breadth_index()
    integrity = snapshot_integrity()

    risk = concentration.get("risk", "unknown")
    gpu_markets = breadth.get("gpu_markets", 0)
    observations = integrity.get("rows", 0)

    if risk == "high":
        regime = "Concentrated Market"
    elif observations < 1000:
        regime = "Early Data Accumulation"
    elif gpu_markets >= 20:
        regime = "Broad GPU Market Coverage"
    else:
        regime = "Developing Market Coverage"

    return {
        "status": "ok",
        "regime": regime,
        "risk": risk,
        "gpu_markets": gpu_markets,
        "observations": observations
    }

@app.get("/terminal-live-coverage-v1")
def terminal_live_coverage_v1():

    from providers.connectors.collector import collect_provider_data

    data = collect_provider_data()
    summary = data.get("summary", {})

    return {
        "status": "ok",
        "total_connectors": summary.get("total_connectors", 0),
        "live_ready": summary.get("live_ready", 0),
        "demo_mode": summary.get("demo_mode", 0),
        "total_normalized_offers": summary.get("total_normalized_offers", 0)
    }

@app.get("/terminal-forecast-signal-v1")
def terminal_forecast_signal_v1():

    from main import terminal_forecast_readiness_v1
    from intelligence.signals.gpu_price_index import (
        calculate_gpu_price_index
    )
    from intelligence.signals.market_supply_index import (
        calculate_market_supply_index
    )

    readiness = terminal_forecast_readiness_v1()
    price = calculate_gpu_price_index()
    supply = calculate_market_supply_index()

    score = readiness.get("forecast_readiness_score", 0)

    if score >= 75:
        signal = "Forecast Ready"
    elif score >= 50:
        signal = "Forecast Warming Up"
    else:
        signal = "Collect More History"

    return {
        "status": "ok",
        "signal": signal,
        "readiness": score,
        "gpu_price_index": price,
        "market_supply": supply
    }

@app.get("/terminal-forecast-intelligence-v1")
def terminal_forecast_intelligence_v1():

    from intelligence.forecast.forecast_engine_v4 import forecast_engine_v4
    from intelligence.forecast.gpu_opportunity_score import gpu_opportunity_score
    from intelligence.forecast.forecast_backtest_summary import forecast_backtest_summary
    from intelligence.forecast.supply_shock_forecast import supply_shock_forecast
    from intelligence.forecast.provider_expansion_forecast import provider_expansion_forecast

    forecasts = forecast_engine_v4()
    opportunities = gpu_opportunity_score()[:10]
    backtest = forecast_backtest_summary()
    shock = supply_shock_forecast()
    expansion = provider_expansion_forecast()

    return {
        "status": "ok",
        "forecast_count": len(forecasts),
        "top_opportunities": opportunities,
        "backtest": backtest,
        "supply_shock": shock,
        "provider_expansion": expansion
    }

@app.get("/terminal-forecast-health-v1")
def terminal_forecast_health_v1():

    from intelligence.forecast.forecast_accuracy_calculation_v1 import (
        forecast_accuracy_calculation_v1
    )

    from intelligence.forecast.forecast_accuracy_dataset import (
        forecast_accuracy_dataset
    )

    accuracy = forecast_accuracy_calculation_v1()
    dataset = forecast_accuracy_dataset()

    return {
        "status": "ok",
        "accuracy": accuracy,
        "dataset": dataset,
        "readout": (
            f"Forecast audit contains {dataset.get('rows', 0)} rows "
            f"across {dataset.get('gpu_models', 0)} GPU models. "
            f"Alpha signal rate is {accuracy.get('alpha_signal_rate', 0)}%."
        )
    }

@app.get("/terminal-data-health-v1")
def terminal_data_health_v1():

    from intelligence.assets.daily_data_health import (
        daily_data_health
    )

    return daily_data_health()

@app.get("/automation-health-v1")
def automation_health_v1():

    from intelligence.operations.collection_health import (
        collection_health
    )

    return collection_health()

@app.get("/terminal-coverage-action-plan-v1")
def terminal_coverage_action_plan_v1():

    from intelligence.coverage.coverage_action_plan import coverage_action_plan
    from intelligence.coverage.provider_coverage_gap import provider_coverage_gap

    return {
        "status": "ok",
        "gap": provider_coverage_gap(),
        "actions": coverage_action_plan()
    }


@app.get("/terminal-historical-asset-health-v1")
def terminal_historical_asset_health_v1():

    from intelligence.assets.historical_asset_health import (
        historical_asset_health
    )

    return historical_asset_health()


@app.get("/terminal-daily-runner-health-v1")
def terminal_daily_runner_health_v1():

    import json
    from pathlib import Path

    latest_file = Path("data/master_daily_cycle_latest.json")
    log_file = Path("logs/master_daily_cycle.log")

    if not latest_file.exists():
        return {
            "status": "missing",
            "latest_file_exists": False,
            "log_file_exists": log_file.exists()
        }

    latest = json.loads(latest_file.read_text())

    return {
        "status": latest.get("status"),
        "latest_file_exists": True,
        "log_file_exists": log_file.exists(),
        "started_at": latest.get("started_at"),
        "finished_at": latest.get("finished_at"),
        "cycle": latest.get("result", {}).get("cycle"),
        "error": latest.get("error")
    }


@app.get("/terminal-collection-health-v2")
def terminal_collection_health_v2():

    from intelligence.operations.collection_health import (
        collection_health
    )

    health = collection_health()

    return {
        "status": "ok",
        "collection": health,
        "headline": f"Collection status is {health.get('status')}",
        "readout": (
            f"{health.get('latest_snapshot_rows', 0)} offers observed "
            f"from {health.get('providers_reporting', 0)} providers. "
            f"Last collection was {health.get('minutes_since_last_collection')} minutes ago."
        )
    }


@app.get("/terminal-forecast-accuracy-v2")
def terminal_forecast_accuracy_v2():

    from intelligence.forecast.forecast_accuracy_v2 import (
        forecast_accuracy_v2
    )

    accuracy = forecast_accuracy_v2()

    return {
        "status": "ok",
        "accuracy": accuracy,
        "headline": f"Forecast Accuracy V2 is {accuracy.get('accuracy_score', 0)}",
        "readout": (
            f"{accuracy.get('correct_rows', 0)} of "
            f"{accuracy.get('forecast_rows', 0)} forecast audit rows match expected signal direction."
        )
    }


@app.get("/terminal-forecast-backtesting-v2")
def terminal_forecast_backtesting_v2():

    from intelligence.forecast.forecast_backtesting_v2 import (
        forecast_backtesting_v2
    )

    backtest = forecast_backtesting_v2()

    return {
        "status": "ok",
        "backtest": backtest,
        "headline": (
            f"Forecast backtest readiness is "
            f"{backtest.get('backtest_readiness_score', 0)}"
        ),
        "readout": (
            f"{backtest.get('forecast_rows', 0)} forecast audit rows across "
            f"{backtest.get('gpu_models', 0)} GPU models."
        )
    }


@app.get("/terminal-forecast-backtesting-v2")
def terminal_forecast_backtesting_v2():

    from intelligence.forecast.forecast_backtesting_v2 import (
        forecast_backtesting_v2
    )

    backtest = forecast_backtesting_v2()

    return {
        "status": "ok",
        "backtest": backtest,
        "headline": (
            f"Forecast backtest readiness is "
            f"{backtest.get('backtest_readiness_score', 0)}"
        ),
        "readout": (
            f"{backtest.get('forecast_rows', 0)} forecast audit rows across "
            f"{backtest.get('gpu_models', 0)} GPU models."
        )
    }


@app.get("/terminal-forecast-accuracy-history-v1")
def terminal_forecast_accuracy_history_v1():

    import pandas as pd
    from pathlib import Path

    file = Path("data/forecast_accuracy_history.csv")

    if not file.exists():
        return {
            "status": "missing",
            "rows": 0
        }

    df = pd.read_csv(file)

    if df.empty:
        return {
            "status": "empty",
            "rows": 0
        }

    latest = df.iloc[-1]

    return {
        "status": "ok",
        "rows": int(len(df)),
        "latest": {
            "timestamp": latest.get("timestamp"),
            "accuracy_score": latest.get("accuracy_score"),
            "forecast_rows": latest.get("forecast_rows"),
            "correct_rows": latest.get("correct_rows")
        }
    }


@app.get("/terminal-forecast-accuracy-trend-v1")
def terminal_forecast_accuracy_trend_v1():

    from intelligence.forecast.forecast_accuracy_trend import (
        forecast_accuracy_trend
    )

    trend = forecast_accuracy_trend()

    return {
        "status": "ok",
        "trend": trend,
        "headline": (
            f"Forecast quality score is "
            f"{trend.get('forecast_quality_score', 0)}"
        ),
        "readout": (
            f"Latest accuracy is {trend.get('latest_accuracy', 0)} "
            f"with trend {trend.get('trend', 'unknown')}."
        )
    }


@app.get("/terminal-data-moat-v2")
def terminal_data_moat_v2():

    from intelligence.signals.data_moat_score_v2 import (
        data_moat_score_v2
    )

    moat = data_moat_score_v2()

    return {
        "status": "ok",
        "data_moat": moat,
        "headline": (
            f"Data moat score is {moat.get('data_moat_score', 0)} "
            f"({moat.get('data_moat_level', 'unknown')})."
        ),
        "readout": (
            f"{len([a for a in moat.get('assets', {}).values() if a.get('rows', 0) > 0])} "
            f"historical assets are active."
        )
    }


@app.get("/terminal-investor-readiness-v1")
def terminal_investor_readiness_v1():

    from intelligence.investor.investor_readiness_score import (
        investor_readiness_score
    )

    readiness = investor_readiness_score()

    return {
        "status": "ok",
        "investor_readiness": readiness,
        "headline": (
            f"Investor readiness is "
            f"{readiness.get('investor_readiness_score', 0)} "
            f"({readiness.get('investor_readiness_level', 'unknown')})."
        ),
        "readout": (
            f"Data moat contributes "
            f"{readiness.get('components', {}).get('data_moat_score', 0)}, "
            f"forecast quality contributes "
            f"{readiness.get('components', {}).get('forecast_quality_score', 0)}."
        )
    }


@app.get("/terminal-investor-readiness-v1")
def terminal_investor_readiness_v1():

    from intelligence.investor.investor_readiness_score import (
        investor_readiness_score
    )

    readiness = investor_readiness_score()

    return {
        "status": "ok",
        "investor_readiness": readiness,
        "headline": (
            f"Investor readiness is "
            f"{readiness.get('investor_readiness_score', 0)} "
            f"({readiness.get('investor_readiness_level', 'unknown')})."
        ),
        "readout": (
            f"Data moat contributes "
            f"{readiness.get('components', {}).get('data_moat_score', 0)}, "
            f"forecast quality contributes "
            f"{readiness.get('components', {}).get('forecast_quality_score', 0)}."
        )
    }


@app.get("/terminal-executive-scorecard-v1")
def terminal_executive_scorecard_v1():

    from intelligence.executive.executive_scorecard_v1 import (
        executive_scorecard_v1
    )

    scorecard = executive_scorecard_v1()

    return {
        "status": "ok",
        "scorecard": scorecard,
        "headline": (
            f"Executive score is {scorecard.get('executive_score', 0)} "
            f"({scorecard.get('executive_level', 'unknown')})."
        ),
        "readout": scorecard.get("readout")
    }


@app.get("/terminal-intelligence-summary-v2")
def terminal_intelligence_summary_v2():

    return {
        "status": "ok",
        "version": "v2",
        "system_health": terminal_system_health_v1(),
        "collection_health": terminal_collection_health_v2(),
        "data_moat": terminal_data_moat_v2(),
        "forecast_accuracy_trend": terminal_forecast_accuracy_trend_v1(),
        "investor_readiness": terminal_investor_readiness_v1(),
        "executive_scorecard": terminal_executive_scorecard_v1(),
        "product_readiness": terminal_product_readiness_v1(),
    }


@app.get("/terminal-product-readiness-v1")
def terminal_product_readiness_v1():

    from intelligence.product.product_readiness_snapshot_v1 import (
        product_readiness_snapshot_v1
    )

    readiness = product_readiness_snapshot_v1()

    return {
        "status": "ok",
        "product_readiness": readiness,
        "headline": (
            f"Product readiness is "
            f"{readiness.get('product_readiness_score', 0)} "
            f"({readiness.get('product_readiness_level', 'unknown')})."
        )
    }


@app.get("/terminal-launchagent-health-v1")
def terminal_launchagent_health_v1():

    import subprocess
    from pathlib import Path

    label = "com.airpct.hourly.collection"

    result = subprocess.run(
        ["launchctl", "list"],
        capture_output=True,
        text=True
    )

    installed = label in result.stdout

    out_log = Path("logs/hourly_collection.launchd.out.log")
    err_log = Path("logs/hourly_collection.launchd.err.log")

    return {
        "status": "ok",
        "label": label,
        "installed": installed,
        "out_log_exists": out_log.exists(),
        "err_log_exists": err_log.exists(),
        "collection": terminal_collection_health_v2().get("collection")
    }


@app.get("/terminal-strategy-dashboard-v1")
def terminal_strategy_dashboard_v1():

    summary = terminal_intelligence_summary_v2()
    launchagent = terminal_launchagent_health_v1()

    product = summary.get("product_readiness", {}).get("product_readiness", {})
    executive = summary.get("executive_scorecard", {}).get("scorecard", {})
    investor = summary.get("investor_readiness", {}).get("investor_readiness", {})
    moat = summary.get("data_moat", {}).get("data_moat", {})
    collection = summary.get("collection_health", {}).get("collection", {})

    product_score = product.get("product_readiness_score", 0)
    executive_score = executive.get("executive_score", 0)
    investor_score = investor.get("investor_readiness_score", 0)
    moat_score = moat.get("data_moat_score", 0)

    if product_score >= 80 and collection.get("healthy") and launchagent.get("installed"):
        stage = "demo_ready"
    elif product_score >= 60:
        stage = "prototype_ready"
    elif product_score >= 40:
        stage = "internal_validation"
    else:
        stage = "early_build"

    next_actions = []

    if not collection.get("healthy"):
        next_actions.append("Fix collection freshness")
    if moat_score < 80:
        next_actions.append("Grow historical data assets")
    if investor_score < 70:
        next_actions.append("Improve investor readiness score")
    if executive_score < 80:
        next_actions.append("Increase executive scorecard strength")

    if not next_actions:
        next_actions.append("Prepare demo narrative and customer discovery")

    strategy = {
        "status": "ok",
        "version": "v1",
        "stage": stage,
        "scores": {
            "product_readiness": product_score,
            "executive_score": executive_score,
            "investor_readiness": investor_score,
            "data_moat": moat_score
        },
        "health": {
            "collection": collection.get("status"),
            "launchagent_installed": launchagent.get("installed")
        },
        "next_actions": next_actions,
        "headline": (
            f"AI-RPCT is currently {stage} with product readiness {product_score}."
        )
    }

    from intelligence.strategy.save_strategy_dashboard_history import (
        save_strategy_dashboard_history
    )

    strategy["history"] = save_strategy_dashboard_history(strategy)

    return strategy


@app.get("/terminal-runbook-v1")
def terminal_runbook_v1():

    from pathlib import Path

    file = Path(
        "docs/runbook_v1.md"
    )

    if not file.exists():
        return {
            "status": "missing",
            "file": str(file)
        }

    return {
        "status": "ok",
        "file": str(file),
        "content": file.read_text()
    }


@app.get("/terminal-operations-dashboard-v1")
def terminal_operations_dashboard_v1():

    from intelligence.operations.operations_dashboard_v1 import (
        operations_dashboard_v1
    )

    dashboard = (
        operations_dashboard_v1()
    )

    return {
        "status": "ok",
        "dashboard": dashboard,
        "headline":
            (
                "Operations dashboard ready"
            )
    }


@app.get("/terminal-ceo-command-center-v1")
def terminal_ceo_command_center_v1():

    strategy = (
        terminal_strategy_dashboard_v1()
    )

    summary = (
        terminal_intelligence_summary_v2()
    )

    operations = (
        terminal_operations_dashboard_v1()
    )

    return {
        "status": "ok",
        "version": "v1",
        "strategy": strategy,
        "summary": summary,
        "operations": operations
    }
