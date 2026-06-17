from providers.connectors.collector import collect_provider_data


def build_gpu_scarcity_index():
    providers = collect_provider_data()

    total_capacity = sum(
        p["available_capacity"]
        for p in providers
    )

    provider_count = len(providers)

    avg_capacity = (
        total_capacity / provider_count
        if provider_count
        else 0
    )

    if avg_capacity >= 100:
        scarcity_score = 20
        scarcity_status = "abundant"

    elif avg_capacity >= 75:
        scarcity_score = 40
        scarcity_status = "healthy"

    elif avg_capacity >= 50:
        scarcity_score = 60
        scarcity_status = "tightening"

    elif avg_capacity >= 25:
        scarcity_score = 80
        scarcity_status = "scarce"

    else:
        scarcity_score = 95
        scarcity_status = "critical"

    return {
        "status": "ok",
        "version": "v1",
        "gpu_scarcity_index": scarcity_score,
        "scarcity_status": scarcity_status,
        "average_capacity": round(avg_capacity, 2),
        "provider_count": provider_count
    }
