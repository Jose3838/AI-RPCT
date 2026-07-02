from __future__ import annotations

from copilot.io import load_csv


def get_historical_intelligence() -> dict:
    return {
        "amd": load_csv("data/amd_historical_gpu_registry.csv"),
        "intel": load_csv("data/intel_historical_gpu_registry.csv"),
        "nvidia": load_csv("data/nvidia_historical_gpu_registry.csv"),
        "pricing": load_csv("data/historical_pricing_registry.csv"),
        "capacity": load_csv("data/historical_capacity_registry.csv"),
        "entities": load_csv("data/historical_entity_registry.csv"),
        "relationships": load_csv("data/historical_relationship_registry.csv"),
        "sources": load_csv("data/historical_source_registry.csv"),
        "gpu_price_history": load_csv("data/gpu_price_history.csv"),
        "live_gpu_price_history": load_csv("data/live_gpu_price_history.csv"),
    }
