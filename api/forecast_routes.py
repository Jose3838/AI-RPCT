from fastapi import APIRouter

from forecast_engine_v2 import build_forecast_engine_v2
from forecast_engine_v3 import build_forecast_engine_v3
from forecast_engine_v31 import build_forecast_engine_v31
from forecast_history import (
    save_forecast_snapshot,
    load_forecast_history
)
from forecast_accuracy_engine import (
    build_forecast_accuracy
)
from forecast_accuracy_v2 import build_forecast_accuracy_v2
from forecast_validation_engine import (
    build_forecast_validation
)
from forecast_error_tracking import build_forecast_error_tracking
from forecast_model_improvement_plan import build_forecast_model_improvement_plan
from forecast_weight_optimization import build_forecast_weight_optimization

router = APIRouter()


@router.get("/forecast-engine-v2")
def forecast_engine_v2():
    return build_forecast_engine_v2()


@router.get("/forecast-engine-v3")
def forecast_engine_v3():
    return build_forecast_engine_v3()


@router.get("/forecast-engine-v31")
def forecast_engine_v31():
    return build_forecast_engine_v31()


@router.post("/save-forecast-snapshot")
def save_forecast_snapshot_endpoint():
    return save_forecast_snapshot()


@router.get("/forecast-history")
def forecast_history_endpoint():
    return {
        "status": "ok",
        "history": load_forecast_history()
    }


@router.get("/forecast-accuracy")
def forecast_accuracy():
    return build_forecast_accuracy()


@router.get("/forecast-accuracy-v2")
def forecast_accuracy_v2():
    return build_forecast_accuracy_v2()


@router.get("/forecast-validation")
def forecast_validation():
    return build_forecast_validation()


@router.get("/forecast-error-tracking")
def forecast_error_tracking():
    return build_forecast_error_tracking()


@router.get("/forecast-model-improvement-plan")
def forecast_model_improvement_plan():
    return build_forecast_model_improvement_plan()


@router.get("/forecast-weight-optimization")
def forecast_weight_optimization():
    return build_forecast_weight_optimization()
