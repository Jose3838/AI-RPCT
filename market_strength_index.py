def calculate_market_strength_index(provider_scores):
    if not provider_scores:
        return {
            "market_strength_index": 0,
            "market_status": "no_data"
        }

    avg_score = sum(provider_scores) / len(provider_scores)
    avg_score = round(avg_score, 2)

    if avg_score >= 85:
        market_status = "very_bullish"
    elif avg_score >= 75:
        market_status = "bullish"
    elif avg_score >= 65:
        market_status = "neutral_positive"
    elif avg_score >= 50:
        market_status = "neutral"
    else:
        market_status = "weak"

    return {
        "market_strength_index": avg_score,
        "market_status": market_status
    }
