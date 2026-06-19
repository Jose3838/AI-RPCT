from intelligence.forecast.forecast_engine_v4 import (
    forecast_engine_v4
)

def gpu_opportunity_score():

    forecasts = forecast_engine_v4()

    result = []

    for row in forecasts:

        recent = row["recent_price"]
        historical = row["historical_price"]

        score = round(
            abs(
                recent - historical
            ) / historical * 100,
            2
        )

        result.append({
            **row,
            "opportunity_score": score
        })

    return sorted(
        result,
        key=lambda x:
            x["opportunity_score"],
        reverse=True
    )
