from provider_coverage_engine_v3 import get_provider_coverage_v3
from providers.connectors.collector import collect_provider_data
from provider_freshness import build_provider_freshness_report


def build_data_trust_index():
    coverage = get_provider_coverage_v3()
    providers = collect_provider_data()
    freshness = build_provider_freshness_report(providers)

    fresh_count = len([
        item
        for item in freshness["providers"]
        if item["freshness_status"] == "fresh"
    ])

    provider_count = len(providers)

    freshness_score = round(
        (fresh_count / provider_count) * 100,
        2
    ) if provider_count else 0

    trust_index = round(
        (
            coverage["coverage_percentage"] * 0.5
            +
            freshness_score * 0.5
        ),
        2
    )

    if trust_index >= 90:
        trust_status = "institutional_grade"
    elif trust_index >= 75:
        trust_status = "enterprise_grade"
    elif trust_index >= 60:
        trust_status = "commercial_grade"
    else:
        trust_status = "early_stage"

    return {
        "status": "ok",
        "version": "v1",
        "data_trust_index": trust_index,
        "trust_status": trust_status,
        "coverage_percentage": coverage["coverage_percentage"],
        "freshness_score": freshness_score,
        "provider_count": provider_count
    }
