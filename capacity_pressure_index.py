from gpu_scarcity_index import build_gpu_scarcity_index
from data_layer.market_strength_pipeline import build_dynamic_market_strength_index
from data_layer.provider_scoring_pipeline import build_dynamic_provider_activation_scores


def build_capacity_pressure_index():
    scarcity = build_gpu_scarcity_index()
    market = build_dynamic_market_strength_index()
    provider_scores = build_dynamic_provider_activation_scores()

    activation_scores = [
        item["activation_score"]
        for item in provider_scores
    ]

    avg_activation = round(
        sum(activation_scores) / len(activation_scores),
        2
    ) if activation_scores else 0

    pressure_index = round(
        (
            scarcity["gpu_scarcity_index"] * 0.50
            +
            market["market_strength_index"] * 0.30
            +
            avg_activation * 0.20
        ),
        2
    )

    if pressure_index >= 80:
        pressure_status = "critical_pressure"
    elif pressure_index >= 65:
        pressure_status = "high_pressure"
    elif pressure_index >= 50:
        pressure_status = "moderate_pressure"
    else:
        pressure_status = "low_pressure"

    return {
        "status": "ok",
        "version": "v1",
        "capacity_pressure_index": pressure_index,
        "pressure_status": pressure_status,
        "scarcity_index": scarcity["gpu_scarcity_index"],
        "market_strength_index": market["market_strength_index"],
        "average_activation_score": avg_activation
    }
