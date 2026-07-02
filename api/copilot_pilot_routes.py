"""Pilot routes backed by the copilot/ service layer.

copilot/ is a typed, tested, independently-built architecture
(Pydantic response models, service layer) that has never been wired
into the deployed app. These two routes are a scoped pilot to test
whether copilot's implementations are viable replacements for their
ad-hoc equivalents (infrastructure_risk_signal.py,
executive_risk_dashboard.py) before committing to a larger migration.
Response shapes intentionally differ from the v1 routes they parallel
copilot's risk/executive intelligence is structured differently
(summary/metrics/risk_drivers/insights) than the v1 flat dicts.
"""

from fastapi import APIRouter

from copilot.service import get_risk_intelligence, get_executive_intelligence

router = APIRouter()


@router.get("/infrastructure-risk-signal-v2")
def infrastructure_risk_signal_v2():
    return get_risk_intelligence()


@router.get("/executive-risk-dashboard-v2")
def executive_risk_dashboard_v2():
    return get_executive_intelligence()
