from fastapi import APIRouter

from executive_intelligence_summary import build_executive_intelligence_summary
from data_layer.executive_intelligence_pipeline import build_dynamic_executive_intelligence_summary
from executive_market_briefing import (
    build_executive_market_briefing
)
from executive_risk_dashboard import (
    build_executive_risk_dashboard
)
from investor_snapshot import build_investor_snapshot
from system_readiness_report import build_system_readiness_report

router = APIRouter()


@router.get("/executive-intelligence-summary")
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


@router.get("/executive-intelligence-summary-v2")
def executive_intelligence_summary_v2():
    return build_dynamic_executive_intelligence_summary()


@router.get("/executive-market-briefing")
def executive_market_briefing():
    return build_executive_market_briefing()


@router.get("/executive-risk-dashboard")
def executive_risk_dashboard():
    return build_executive_risk_dashboard()


@router.get("/investor-snapshot-v2")
def investor_snapshot_v2():
    return build_investor_snapshot()


@router.get("/system-readiness-report")
def system_readiness_report():
    return build_system_readiness_report()
