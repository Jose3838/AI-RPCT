from main import (
    terminal_intelligence_summary_v1,
    terminal_market_narrative_v1,
    terminal_investor_snapshot_v1,
    terminal_data_moat_v1,
    terminal_signal_tape_v1,
    terminal_market_movers_v1,
    terminal_provider_risk_v1,
    terminal_forecast_readiness_v1,
    terminal_system_health_v1,
    terminal_demo_warning_v1,
)

CHECKS = {
    "terminal_intelligence_summary_v1": terminal_intelligence_summary_v1,
    "terminal_market_narrative_v1": terminal_market_narrative_v1,
    "terminal_investor_snapshot_v1": terminal_investor_snapshot_v1,
    "terminal_data_moat_v1": terminal_data_moat_v1,
    "terminal_signal_tape_v1": terminal_signal_tape_v1,
    "terminal_market_movers_v1": terminal_market_movers_v1,
    "terminal_provider_risk_v1": terminal_provider_risk_v1,
    "terminal_forecast_readiness_v1": terminal_forecast_readiness_v1,
    "terminal_system_health_v1": terminal_system_health_v1,
    "terminal_demo_warning_v1": terminal_demo_warning_v1,
}

def run():
    failures = []

    for name, fn in CHECKS.items():
        try:
            result = fn()
            if not isinstance(result, dict):
                failures.append((name, "result is not dict"))
            else:
                print(f"OK {name}")
        except Exception as error:
            failures.append((name, str(error)))

    if failures:
        print("\nFAILURES")
        for name, error in failures:
            print(f"{name}: {error}")
        raise SystemExit(1)

    print("\nUI SMOKE TEST PASSED")

if __name__ == "__main__":
    run()
