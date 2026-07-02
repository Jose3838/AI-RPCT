from fastapi import APIRouter

from connector_health_dashboard import build_connector_health_dashboard
from live_data_readiness_score import build_live_data_readiness_score
from connector_maturity_dashboard import (
    build_connector_maturity_dashboard
)
from connector_coverage_score import build_connector_coverage_score
from live_data_migration_plan import build_live_data_migration_plan
from live_data_migration_dashboard import build_live_data_migration_dashboard
from live_data_quality_v2 import build_live_data_quality_v2
from connector_portfolio_score import (
    build_connector_portfolio_score
)
from historical_live_data_coverage import (
    build_historical_live_data_coverage
)
from live_data_snapshot_auditor import build_live_data_snapshot_audit
from live_data_audit_history import (
    save_live_data_audit_snapshot,
    load_live_data_audit_history
)

router = APIRouter()


@router.get("/connector-health-dashboard")
def connector_health_dashboard():
    return build_connector_health_dashboard()


@router.get("/live-data-readiness-score")
def live_data_readiness_score():
    return build_live_data_readiness_score()


@router.get("/connector-maturity-dashboard")
def connector_maturity_dashboard():
    return build_connector_maturity_dashboard()


@router.get("/connector-coverage-score")
def connector_coverage_score():
    return build_connector_coverage_score()


@router.get("/live-data-migration-plan")
def live_data_migration_plan():
    return build_live_data_migration_plan()


@router.get("/live-data-migration-dashboard")
def live_data_migration_dashboard():
    return build_live_data_migration_dashboard()


@router.get("/live-data-quality-v2")
def live_data_quality_v2():
    return build_live_data_quality_v2()


@router.get("/connector-portfolio-score")
def connector_portfolio_score():
    return build_connector_portfolio_score()


@router.get("/historical-live-data-coverage")
def historical_live_data_coverage():
    return build_historical_live_data_coverage()


@router.get("/live-data-snapshot-audit")
def live_data_snapshot_audit():
    return build_live_data_snapshot_audit()


@router.post("/save-live-data-audit-snapshot")
def save_live_data_audit_snapshot_endpoint():
    return save_live_data_audit_snapshot()


@router.get("/live-data-audit-history")
def live_data_audit_history_endpoint():
    return {
        "status": "ok",
        "history": load_live_data_audit_history()
    }
