from intelligence.signals.provider_supply_share import (
    provider_supply_share
)


def provider_switching_advisor_v1():
    shares = provider_supply_share()

    if not shares:
        return {
            "status": "no_provider_data",
            "decision": "unknown"
        }

    leader = shares[0]
    alternatives = shares[1:4]

    leader_share = float(
        leader.get("market_share_pct", 0)
    )

    if leader_share >= 85:
        decision = "diversify"
        reason = (
            f"{leader.get('provider')} dominates with "
            f"{leader_share}% market share. Consider testing alternatives."
        )
    elif leader_share >= 60:
        decision = "monitor_concentration"
        reason = (
            f"{leader.get('provider')} leads with "
            f"{leader_share}% market share. Monitor concentration risk."
        )
    else:
        decision = "balanced_market"
        reason = "Provider market appears reasonably balanced."

    return {
        "status": "ok",
        "version": "v1",
        "decision": decision,
        "leader": leader,
        "alternatives": alternatives,
        "reason": reason
    }
