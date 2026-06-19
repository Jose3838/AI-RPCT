from intelligence.history.save_gpu_daily_state import (
    save_gpu_daily_state
)

from intelligence.providers.save_provider_market_share import (
    save_provider_market_share
)

from intelligence.forecast.save_forecast_audit import (
    save_forecast_audit
)

from intelligence.coverage.save_live_coverage_history import (
    save_live_coverage_history
)

def run_master_intelligence_collector():

    gpu = save_gpu_daily_state()

    providers = (
        save_provider_market_share()
    )

    forecast = (
        save_forecast_audit()
    )

    coverage = (
        save_live_coverage_history()
    )

    return {
        "gpu_state": gpu,
        "providers": providers,
        "forecast": forecast,
        "coverage": coverage
    }
