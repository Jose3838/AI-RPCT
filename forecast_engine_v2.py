from trend_intelligence import build_trend_intelligence


def build_forecast_engine_v2():
    trend = build_trend_intelligence()

    if trend.get("status") != "ok":
        return {
            "status": "not_enough_data"
        }

    change = trend["market_strength_change"]

    if change > 5:
        signal = "strong_growth_expected"
        confidence = "high"

    elif change > 0:
        signal = "moderate_growth_expected"
        confidence = "medium"

    elif change < -5:
        signal = "market_weakness_expected"
        confidence = "high"

    elif change < 0:
        signal = "slight_weakness_expected"
        confidence = "medium"

    else:
        signal = "stable_market_expected"
        confidence = "medium"

    return {
        "status": "ok",
        "version": "v2",
        "forecast_signal": signal,
        "confidence": confidence,
        "market_strength_change": change
    }
