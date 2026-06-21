from intelligence.coverage.provider_coverage_gap import provider_coverage_gap

PRIORITY = {
    "nebius": 1,
    "coreweave": 2,
    "crusoe": 3,
    "lambda": 4,
    "runpod": 5,
    "vast": 6,
}

def coverage_action_plan():

    gap = provider_coverage_gap()

    actions = []

    for item in gap["gaps"]:

        provider = item["provider"]

        actions.append({
            "provider": provider,
            "priority": PRIORITY.get(provider, 99),
            "current_mode": item["mode"],
            "recommended_action": f"Add valid {provider.upper()} API key or implement live market fetch"
        })

    return sorted(
        actions,
        key=lambda x: x["priority"]
    )
