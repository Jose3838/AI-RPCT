from fastapi import APIRouter

from intelligence_quality_dashboard import build_intelligence_quality_dashboard
from prediction_research_dashboard import (
    build_prediction_research_dashboard
)
from data_moat_dashboard import (
    build_data_moat_dashboard
)
from intelligence_performance_dashboard import (
    build_intelligence_performance_dashboard
)
from data_moat_growth_plan import build_data_moat_growth_plan
from history_schema_health import build_history_schema_health

router = APIRouter()


@router.get("/intelligence-quality-dashboard")
def intelligence_quality_dashboard():
    return build_intelligence_quality_dashboard()


@router.get("/prediction-research-dashboard")
def prediction_research_dashboard():
    return build_prediction_research_dashboard()


@router.get("/data-moat-dashboard")
def data_moat_dashboard():
    return build_data_moat_dashboard()


@router.get("/intelligence-performance-dashboard")
def intelligence_performance_dashboard():
    return build_intelligence_performance_dashboard()


@router.get("/data-moat-growth-plan")
def data_moat_growth_plan():
    return build_data_moat_growth_plan()


@router.get("/history-schema-health")
def history_schema_health():
    return build_history_schema_health()
