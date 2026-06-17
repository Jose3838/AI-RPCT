from providers.connectors.collector import collect_provider_data


def build_live_data_quality_v2():
    providers = collect_provider_data()

    results = []

    for item in providers:
        source = item.get("source", "")

        is_live = "live_api" in source
        has_capacity = item.get("available_capacity", 0) > 0
        has_price = item.get("price_per_hour", 0) > 0
        has_gpu_type = bool(item.get("gpu_type"))

        quality_score = 0

        if is_live:
            quality_score += 40
        if has_capacity:
            quality_score += 25
        if has_price:
            quality_score += 25
        if has_gpu_type:
            quality_score += 10

        results.append({
            "provider": item["provider"],
            "source": source,
            "quality_score": quality_score,
            "is_live": is_live,
            "has_capacity": has_capacity,
            "has_price": has_price,
            "has_gpu_type": has_gpu_type
        })

    avg_quality = round(
        sum(item["quality_score"] for item in results) / len(results),
        2
    ) if results else 0

    return {
        "status": "ok",
        "version": "v2",
        "average_live_data_quality": avg_quality,
        "providers": results
    }
