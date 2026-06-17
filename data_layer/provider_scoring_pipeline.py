from data_layer.provider_data_pipeline import build_provider_dataset
from provider_activation_score import calculate_provider_activation_score


def price_to_score(price_per_hour):
    if price_per_hour <= 0.40:
        return 95
    elif price_per_hour <= 0.50:
        return 88
    elif price_per_hour <= 0.75:
        return 75
    elif price_per_hour <= 1.00:
        return 60
    else:
        return 40


def capacity_to_score(available_capacity):
    if available_capacity >= 150:
        return 95
    elif available_capacity >= 100:
        return 88
    elif available_capacity >= 50:
        return 75
    elif available_capacity >= 20:
        return 60
    else:
        return 40


def momentum_to_score(provider):
    momentum_map = {
        "vast": 74,
        "runpod": 76,
        "coreweave": 70,
        "lambda": 70,
        "nebius": 70,
        "crusoe": 70
    }

    return momentum_map.get(provider, 60)


def build_dynamic_provider_activation_scores():
    dataset = build_provider_dataset()

    results = []

    for item in dataset:
        price_score = price_to_score(item["price_per_hour"])
        capacity_score = capacity_to_score(item["available_capacity"])
        health_score = item["health_score"]
        momentum_score = momentum_to_score(item["provider"])

        score = calculate_provider_activation_score(
            price_score,
            capacity_score,
            health_score,
            momentum_score
        )

        results.append({
            "provider": item["provider"],
            "gpu_type": item["gpu_type"],
            "region": item["region"],
            "source": item["source"],
            **score
        })

    return results
