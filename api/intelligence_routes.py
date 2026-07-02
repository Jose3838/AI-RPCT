from fastapi import APIRouter

from automated_snapshot_runner import run_daily_snapshot
from historical_query_api import get_historical_data
from trend_intelligence import build_trend_intelligence
from gpu_scarcity_index import build_gpu_scarcity_index
from capacity_pressure_index import build_capacity_pressure_index
from infrastructure_risk_signal import build_infrastructure_risk_signal
from historical_intelligence_engine import build_historical_intelligence
from intelligence_registry import build_intelligence_registry
from historical_intelligence_v2 import (
    build_historical_intelligence_v2
)
from gpu_scarcity_history import (
    save_gpu_scarcity_snapshot,
    load_gpu_scarcity_history
)
from historical_intelligence_score import (
    build_historical_intelligence_score
)
from capacity_pressure_history import (
    save_capacity_pressure_snapshot,
    load_capacity_pressure_history
)
from risk_signal_history import (
    save_risk_signal_snapshot,
    load_risk_signal_history
)
from automated_intelligence_snapshot_v2 import run_intelligence_snapshot_v2

router = APIRouter()


@router.post("/run-daily-snapshot")
def run_daily_snapshot_endpoint():
    return run_daily_snapshot()


@router.get("/historical-data")
def historical_data():
    return get_historical_data()


@router.get("/trend-intelligence")
def trend_intelligence():
    return build_trend_intelligence()


@router.get("/gpu-scarcity-index")
def gpu_scarcity_index():
    return build_gpu_scarcity_index()


@router.get("/capacity-pressure-index")
def capacity_pressure_index():
    return build_capacity_pressure_index()


@router.get("/infrastructure-risk-signal")
def infrastructure_risk_signal():
    return build_infrastructure_risk_signal()


@router.get("/historical-intelligence")
def historical_intelligence():
    return build_historical_intelligence()


@router.get("/intelligence-registry")
def intelligence_registry():
    return build_intelligence_registry()


@router.get("/historical-intelligence-v2")
def historical_intelligence_v2():
    return build_historical_intelligence_v2()


@router.post("/save-gpu-scarcity-snapshot")
def save_gpu_scarcity_snapshot_endpoint():
    return save_gpu_scarcity_snapshot()


@router.get("/gpu-scarcity-history")
def gpu_scarcity_history_endpoint():
    return {
        "status": "ok",
        "history": load_gpu_scarcity_history()
    }


@router.get("/historical-intelligence-score")
def historical_intelligence_score():
    return build_historical_intelligence_score()


@router.post("/save-capacity-pressure-snapshot")
def save_capacity_pressure_snapshot_endpoint():
    return save_capacity_pressure_snapshot()


@router.get("/capacity-pressure-history")
def capacity_pressure_history_endpoint():
    return {
        "status": "ok",
        "history": load_capacity_pressure_history()
    }


@router.post("/save-risk-signal-snapshot")
def save_risk_signal_snapshot_endpoint():
    return save_risk_signal_snapshot()


@router.get("/risk-signal-history")
def risk_signal_history_endpoint():
    return {
        "status": "ok",
        "history": load_risk_signal_history()
    }


@router.post("/run-intelligence-snapshot-v2")
def run_intelligence_snapshot_v2_endpoint():
    return run_intelligence_snapshot_v2()
