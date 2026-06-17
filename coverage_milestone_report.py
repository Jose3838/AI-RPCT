from provider_coverage_engine_v3 import get_provider_coverage_v3
from providers.connectors.collector import collect_provider_data


def build_coverage_milestone_report():
    coverage = get_provider_coverage_v3()
    providers = collect_provider_data()

    if coverage["coverage_percentage"] >= 100:
        milestone = "target_provider_coverage_complete"
        business_signal = "enterprise_market_coverage_ready"
    elif coverage["coverage_percentage"] >= 80:
        milestone = "bloomberg_grade_coverage"
        business_signal = "strong_enterprise_signal"
    elif coverage["coverage_percentage"] >= 50:
        milestone = "expanding_coverage"
        business_signal = "commercially_promising"
    else:
        milestone = "early_coverage"
        business_signal = "data_moat_still_early"

    return {
        "status": "ok",
        "version": "v1",
        "milestone": milestone,
        "business_signal": business_signal,
        "coverage": coverage,
        "tracked_providers": [
            item["provider"]
            for item in providers
        ],
        "cto_recommendation": "Start automated daily snapshots and convert enterprise reports into gated paid assets."
    }
