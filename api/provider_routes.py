import csv

from fastapi import APIRouter

from provider_coverage_engine_v3 import get_provider_coverage_v3
from provider_activation_score import (
    calculate_provider_activation_score
)
from provider_expansion_tracker import save_provider_expansion
from data_layer.provider_data_pipeline import build_provider_dataset
from data_layer.provider_scoring_pipeline import build_dynamic_provider_activation_scores
from providers.connectors.collector import (
    collect_provider_data
)
from provider_freshness import build_provider_freshness_report
from provider_ranking_engine import build_provider_ranking
from provider_recommendation_engine import build_provider_recommendations
from provider_concentration_risk import (
    build_provider_concentration_risk
)
from provider_api_key_readiness import build_provider_api_key_readiness

router = APIRouter()


@router.get("/history-provider-activation")
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


@router.get("/provider-coverage-v3")
def provider_coverage_v3():
    return get_provider_coverage_v3()


@router.get("/provider-activation-score")
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


@router.post("/save-provider-expansion")
def save_provider_expansion_endpoint():
    return save_provider_expansion()


@router.get("/unified-provider-data")
def unified_provider_data():
    return {
        "status": "ok",
        "records": build_provider_dataset()
    }


@router.get("/provider-activation-score-v2")
def provider_activation_score_v2():
    return {
        "status": "ok",
        "version": "v2",
        "providers": build_dynamic_provider_activation_scores()
    }


@router.get("/provider-collector")
def provider_collector():
    return {
        "status": "ok",
        "providers": collect_provider_data()
    }


@router.post("/save-provider-expansion-v2")
def save_provider_expansion_v2():
    return save_provider_expansion()


@router.get("/provider-freshness")
def provider_freshness():
    providers = collect_provider_data()
    return build_provider_freshness_report(providers)


@router.get("/provider-ranking")
def provider_ranking():
    return build_provider_ranking()


@router.get("/provider-recommendations")
def provider_recommendations():
    return build_provider_recommendations()


@router.get("/provider-concentration-risk")
def provider_concentration_risk():
    return build_provider_concentration_risk()


@router.get("/provider-api-key-readiness")
def provider_api_key_readiness():
    return build_provider_api_key_readiness()
