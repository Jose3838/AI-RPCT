from investor_snapshot import build_investor_snapshot


def build_provider_concentration_risk():

    snapshot = build_investor_snapshot()

    shares = snapshot.get(
        "provider_market_share",
        []
    )

    if not shares:
        return {
            "status": "no_data"
        }

    largest_share = max(
        item["market_share_pct"]
        for item in shares
    )

    if largest_share >= 70:
        risk = "critical"

    elif largest_share >= 50:
        risk = "high"

    elif largest_share >= 30:
        risk = "moderate"

    else:
        risk = "low"

    return {
        "status": "ok",
        "version": "v1",
        "largest_provider_share": largest_share,
        "concentration_risk": risk
    }
