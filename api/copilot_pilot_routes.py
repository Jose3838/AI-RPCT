"""Pilot routes backed by the copilot/ service layer.

copilot/ is a typed, tested, independently-built architecture
(Pydantic response models, service layer) that has never been wired
into the deployed app. Started as a scoped pilot for two risk/executive
routes to test whether copilot's implementations are viable
replacements for their ad-hoc equivalents (infrastructure_risk_signal.py,
executive_risk_dashboard.py) before committing to a larger migration.
Response shapes intentionally differ from the v1 routes they parallel
copilot's intelligence is structured differently (summary/metrics/
insights) than the v1 flat dicts.

Sprint 6 (Decision Intelligence) added two more: /capacity-advisor
(real current-state capacity pressure assessment, not a demand
forecast) and /procurement-optimizer (cloud vs. on-prem breakeven for
NVIDIA H100, the only GPU with both a real purchase-price anchor and
real cloud rates in this repo's data - a static calculation, not a
price-trend prediction).
"""

from fastapi import APIRouter

from copilot.service import (
    get_risk_intelligence,
    get_executive_intelligence,
    get_capacity_intelligence,
    get_procurement_optimizer,
)

router = APIRouter()


@router.get("/infrastructure-risk-signal-v2")
def infrastructure_risk_signal_v2():
    return get_risk_intelligence()


@router.get("/executive-risk-dashboard-v2")
def executive_risk_dashboard_v2():
    return get_executive_intelligence()


@router.get("/capacity-advisor")
def capacity_advisor():
    return get_capacity_intelligence()


@router.get("/procurement-optimizer")
def procurement_optimizer():
    return get_procurement_optimizer()
