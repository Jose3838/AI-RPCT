from automated_snapshot_runner import run_daily_snapshot
from gpu_scarcity_history import save_gpu_scarcity_snapshot
from capacity_pressure_history import save_capacity_pressure_snapshot
from risk_signal_history import save_risk_signal_snapshot
from forecast_history import save_forecast_snapshot


def run_intelligence_snapshot_v2():
    daily = run_daily_snapshot()
    scarcity = save_gpu_scarcity_snapshot()
    pressure = save_capacity_pressure_snapshot()
    risk = save_risk_signal_snapshot()
    forecast = save_forecast_snapshot()

    return {
        "status": "ok",
        "version": "v2",
        "daily_snapshot": daily,
        "gpu_scarcity_snapshot": scarcity,
        "capacity_pressure_snapshot": pressure,
        "risk_signal_snapshot": risk,
        "forecast_snapshot": forecast
    }
