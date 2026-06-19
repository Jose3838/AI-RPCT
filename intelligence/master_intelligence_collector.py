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

from intelligence.regime.save_market_regime_history import (
    save_market_regime_history
)

from intelligence.regime.save_provider_dominance_history import (
    save_provider_dominance_history
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

    regime = (
        save_market_regime_history()
    )

    provider_dominance = (
        save_provider_dominance_history()
    )

    return {
        "gpu_state": gpu,
        "providers": providers,
        "forecast": forecast,
        "coverage": coverage,
        "regime": regime,
        "provider_dominance": provider_dominance
    }
