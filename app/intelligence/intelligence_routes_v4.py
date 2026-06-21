from fastapi import APIRouter
from app.intelligence.intelligence_core_v4 import (
    compute_market_regime,
    compute_provider_relative_strength,
    compute_provider_early_warning,
    compute_forecast_attribution,
    compute_market_signal_score,
    run_intelligence_snapshot_v4,
)

router = APIRouter(tags=["Intelligence Core v4"])

@router.get("/market-regime")
def market_regime():
    return compute_market_regime()

@router.get("/provider-relative-strength")
def provider_relative_strength():
    return compute_provider_relative_strength()

@router.get("/provider-early-warning")
def provider_early_warning():
    return compute_provider_early_warning()

@router.get("/forecast-attribution")
def forecast_attribution():
    return compute_forecast_attribution()

@router.get("/market-signal-score")
def market_signal_score():
    return compute_market_signal_score()

@router.get("/run-intelligence-snapshot-v4")
def intelligence_snapshot_v4():
    return run_intelligence_snapshot_v4()
