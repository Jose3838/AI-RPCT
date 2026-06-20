from intelligence.history.save_gpu_daily_state import (
    save_gpu_daily_state
)

from intelligence.providers.save_provider_market_share import (
    save_provider_market_share
)

from intelligence.forecast.save_forecast_audit import (
    save_forecast_audit
)

from intelligence.forecast.save_forecast_snapshot import (
    save_forecast_snapshot
)

from intelligence.forecast.save_forecast_accuracy_history import (
    save_forecast_accuracy_history
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

from intelligence.market_depth.save_market_depth_history import (
    save_market_depth_history
)

from intelligence.features.daily_feature_store import (
    append_daily_features
)

def run_master_intelligence_collector():

    gpu = save_gpu_daily_state()

    providers = (
        save_provider_market_share()
    )

    forecast = (
        save_forecast_audit()
    )

    forecast_snapshot = (
        save_forecast_snapshot()
    )

    forecast_accuracy = (
        save_forecast_accuracy_history()
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

    market_depth = (
        save_market_depth_history()
    )

    features = (
        append_daily_features()
    )

    return {
        "gpu_state": gpu,
        "providers": providers,
        "forecast": forecast,
        "forecast_snapshot": forecast_snapshot,
        "forecast_accuracy": forecast_accuracy,
        "coverage": coverage,
        "regime": regime,
        "provider_dominance": provider_dominance,
        "market_depth": market_depth,
        "features": features
    }
