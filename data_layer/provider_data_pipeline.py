from data_layer.unified_provider_schema import normalize_provider_data
from providers.connectors.collector import collect_provider_data


def build_provider_dataset():
    raw_provider_data = collect_provider_data()

    return [
        normalize_provider_data(
            provider=item["provider"],
            gpu_type=item["gpu_type"],
            price_per_hour=item["price_per_hour"],
            available_capacity=item["available_capacity"],
            health_score=item["health_score"],
            region=item["region"],
            source=f'{item["provider"]}_connector'
        )
        for item in raw_provider_data
    ]
