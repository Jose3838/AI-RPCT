from intelligence.executive.executive_scorecard_v1 import executive_scorecard_v1
from intelligence.investor.investor_readiness_score import investor_readiness_score
from intelligence.signals.data_moat_score_v2 import data_moat_score_v2
from intelligence.operations.collection_health import collection_health


def product_readiness_snapshot_v1():
    executive = executive_scorecard_v1()
    investor = investor_readiness_score()
    moat = data_moat_score_v2()
    collection = collection_health()

    score = round(
        executive.get("executive_score", 0) * 0.35
        + investor.get("investor_readiness_score", 0) * 0.25
        + moat.get("data_moat_score", 0) * 0.25
        + (100 if collection.get("healthy") else 0) * 0.15,
        2
    )

    if score >= 80:
        level = "sellable"
    elif score >= 60:
        level = "demo_ready"
    elif score >= 40:
        level = "prototype_ready"
    else:
        level = "internal_only"

    return {
        "status": "ok",
        "version": "v1",
        "product_readiness_score": score,
        "product_readiness_level": level,
        "components": {
            "executive_score": executive.get("executive_score", 0),
            "investor_readiness_score": investor.get("investor_readiness_score", 0),
            "data_moat_score": moat.get("data_moat_score", 0),
            "collection_healthy": collection.get("healthy", False)
        }
    }
