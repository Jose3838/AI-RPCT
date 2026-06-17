def normalize_provider_data(
    provider,
    gpu_type,
    price_per_hour,
    available_capacity,
    health_score,
    region,
    source
):
    return {
        "provider": provider,
        "gpu_type": gpu_type,
        "price_per_hour": float(price_per_hour),
        "available_capacity": int(available_capacity),
        "health_score": float(health_score),
        "region": region,
        "source": source
    }
