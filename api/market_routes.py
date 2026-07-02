from fastapi import APIRouter

from market_strength_index import calculate_market_strength_index
from daily_market_snapshot import save_market_snapshot
from data_layer.market_strength_pipeline import build_dynamic_market_strength_index
from data_layer.dynamic_snapshot_pipeline import save_dynamic_market_snapshot
from data_layer.trend_engine import build_market_trend_summary
from weekly_infrastructure_report import build_weekly_infrastructure_report

router = APIRouter()


@router.get("/market-strength-index")
def market_strength_index():
    provider_scores = [
        85.3,
        84.2
    ]

    return calculate_market_strength_index(provider_scores)


@router.post("/save-market-snapshot")
def save_market_snapshot_endpoint():

    coverage = 33.33
    market_strength = 84.75
    avg_activation_score = 84.75

    return save_market_snapshot(
        coverage,
        market_strength,
        avg_activation_score
    )


@router.get("/market-strength-index-v2")
def market_strength_index_v2():
    return build_dynamic_market_strength_index()


@router.post("/save-market-snapshot-v2")
def save_market_snapshot_v2():
    return save_dynamic_market_snapshot()


@router.get("/market-trend-summary")
def market_trend_summary():
    return build_market_trend_summary()


@router.get("/weekly-infrastructure-report")
def weekly_infrastructure_report():
    return build_weekly_infrastructure_report()
