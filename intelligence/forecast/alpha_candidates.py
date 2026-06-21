from intelligence.forecast.forecast_engine_v4 import (
    forecast_engine_v4
)

def alpha_candidates():

    forecasts = forecast_engine_v4()

    return [
        x
        for x in forecasts
        if x["signal"] != "neutral"
    ]
