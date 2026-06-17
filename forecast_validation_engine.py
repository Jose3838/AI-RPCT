from forecast_validation_store import (
    load_forecasts,
    load_market_history
)


def build_forecast_validation():
    forecasts = load_forecasts()
    market = load_market_history()

    return {
        "status": "ok",
        "forecast_records": len(forecasts),
        "market_records": len(market),
        "validation_ready": (
            len(forecasts) >= 2
            and
            len(market) >= 2
        )
    }
