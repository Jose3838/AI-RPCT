from __future__ import annotations

from copilot.io import load_csv


def get_historical_intelligence() -> dict:
    amd = load_csv("data/amd_historical_gpu_registry.csv")
    intel = load_csv("data/intel_historical_gpu_registry.csv")
    nvidia = load_csv("data/nvidia_historical_gpu_registry.csv")
    pricing = load_csv("data/historical_pricing_registry.csv")
    performance = load_csv("data/historical_performance_registry.csv")
    capacity = load_csv("data/historical_capacity_registry.csv")
    entities = load_csv("data/historical_entity_registry.csv")
    relationships = load_csv("data/historical_relationship_registry.csv")
    sources = load_csv("data/historical_source_registry.csv")
    gpu_price_history = load_csv("data/gpu_price_history.csv")
    live_gpu_price_history = load_csv("data/live_gpu_price_history.csv")
    cloud_gpu_price_history = load_csv("data/cloud_gpu_price_history.csv")
    supply_chain_events = load_csv("data/supply_chain_event_registry.csv")
    open_source_releases = load_csv("data/open_source_framework_registry.csv")

    launch_years = []

    for rows in (amd, intel, nvidia):
        for row in rows:
            year = row.get("launch_year")
            if year and year.isdigit():
                launch_years.append(int(year))

    market_start_year = min(launch_years) if launch_years else None
    market_latest_year = max(launch_years) if launch_years else None

    years_covered = (
        market_latest_year - market_start_year + 1
        if market_start_year and market_latest_year
        else 0
    )

    return {
        "summary": {
            "vendors": 3,
            "market_start_year": market_start_year,
            "market_latest_year": market_latest_year,
            "years_covered": years_covered,
            "gpu_records": len(amd) + len(intel) + len(nvidia),
            "pricing_records": len(pricing),
            "performance_records": len(performance),
            "capacity_records": len(capacity),
            "entity_records": len(entities),
            "relationship_records": len(relationships),
            "source_records": len(sources),
            "gpu_price_history_records": len(gpu_price_history),
            "live_gpu_price_history_records": len(live_gpu_price_history),
            "cloud_gpu_price_history_records": len(cloud_gpu_price_history),
            "supply_chain_event_records": len(supply_chain_events),
            "open_source_release_records": len(open_source_releases),
        },
        "amd": amd,
        "intel": intel,
        "nvidia": nvidia,
        "pricing": pricing,
        "performance": performance,
        "capacity": capacity,
        "entities": entities,
        "relationships": relationships,
        "sources": sources,
        "gpu_price_history": gpu_price_history,
        "live_gpu_price_history": live_gpu_price_history,
        "cloud_gpu_price_history": cloud_gpu_price_history,
        "supply_chain_events": supply_chain_events,
        "open_source_releases": open_source_releases,
    }
