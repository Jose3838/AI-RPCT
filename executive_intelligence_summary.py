def build_executive_intelligence_summary(
    coverage,
    activation_scores,
    market_strength
):
    avg_activation_score = round(
        sum(activation_scores) / len(activation_scores),
        2
    ) if activation_scores else 0

    if market_strength >= 85:
        executive_signal = "aggressive_expansion"
    elif market_strength >= 75:
        executive_signal = "market_opportunity_strong"
    elif market_strength >= 65:
        executive_signal = "selective_expansion"
    elif market_strength >= 50:
        executive_signal = "monitor_market"
    else:
        executive_signal = "risk_off"

    return {
        "product": "AI-RPCT",
        "version": "v6.2",
        "category": "AI Infrastructure Intelligence",
        "coverage_percentage": coverage,
        "average_provider_activation_score": avg_activation_score,
        "market_strength_index": market_strength,
        "executive_signal": executive_signal,
        "enterprise_readiness": "high",
        "recommended_action": (
            "Prioritize provider expansion, historical data capture, and enterprise reporting."
        )
    }
