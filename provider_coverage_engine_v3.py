from providers.provider_registry import PROVIDERS


def get_provider_coverage_v3():
    total = len(PROVIDERS)

    live = len([
        provider
        for provider in PROVIDERS.values()
        if provider["status"] == "live"
    ])

    planned = len([
        provider
        for provider in PROVIDERS.values()
        if provider["status"] == "planned"
    ])

    coverage = round((live / total) * 100, 2)

    return {
        "live_providers": live,
        "planned_providers": planned,
        "total_target_providers": total,
        "coverage_percentage": coverage,
        "coverage_status": (
            "early_market_coverage"
            if coverage < 50
            else "expanding_market_coverage"
            if coverage < 80
            else "bloomberg_grade_coverage"
        )
    }
