from __future__ import annotations

from pathlib import Path

import pandas as pd

FORECASTS = Path("data/forecast_engine_v1.csv")
REGIMES = Path("data/market_regime_v1.csv")
OUT = Path("data/forecast_backtest_v1.csv")
REPORT = Path("reports/forecast_backtest_v1.md")


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size <= 1:
        return pd.DataFrame()
    return pd.read_csv(path)


def expected_outcome(signal: str) -> str:
    if signal == "volatile_market":
        return "volatile_market"
    if signal == "price_pressure_possible":
        return "tight_market"
    if signal == "stable_market":
        return "stable_market"
    return "unknown"


def main() -> None:
    forecasts = read_csv(FORECASTS)
    regimes = read_csv(REGIMES)

    if forecasts.empty:
        raise SystemExit("forecast_engine_v1.csv missing or empty")
    if regimes.empty:
        raise SystemExit("market_regime_v1.csv missing or empty")

    merged = forecasts.merge(
        regimes[["provider", "gpu", "market_regime"]],
        on=["provider", "gpu"],
        how="left",
    )

    rows = []

    for _, row in merged.iterrows():
        expected = expected_outcome(str(row.get("forecast_signal", "")))
        observed = str(row.get("market_regime", "unknown"))

        if expected == "unknown" or observed in {"nan", "unknown"}:
            result = "not_evaluable"
        elif expected == observed:
            result = "directionally_correct"
        else:
            result = "needs_future_validation"

        rows.append({
            "provider": row.get("provider"),
            "gpu": row.get("gpu"),
            "forecast_signal": row.get("forecast_signal"),
            "expected_outcome": expected,
            "observed_regime": observed,
            "confidence": row.get("confidence"),
            "backtest_result": result,
        })

    out = pd.DataFrame(rows)
    OUT.parent.mkdir(exist_ok=True)
    REPORT.parent.mkdir(exist_ok=True)
    out.to_csv(OUT, index=False)

    evaluable = out[out["backtest_result"] != "not_evaluable"]
    correct = int((evaluable["backtest_result"] == "directionally_correct").sum()) if not evaluable.empty else 0
    accuracy = round(correct / len(evaluable), 4) if len(evaluable) else 0

    REPORT.write_text(
        "\n".join([
            "# Forecast Backtester v1",
            "",
            f"Forecasts evaluated: {len(out)}",
            f"Evaluable forecasts: {len(evaluable)}",
            f"Directionally correct: {correct}",
            f"Directional accuracy proxy: {accuracy}",
            "",
            "This is an early proxy backtest. True future-outcome validation begins once forecast snapshots age against future market observations.",
            "",
        ]),
        encoding="utf-8",
    )

    print("FORECAST BACKTESTER V1")
    print("======================")
    print(f"Forecasts evaluated: {len(out)}")
    print(f"Evaluable forecasts: {len(evaluable)}")
    print(f"Accuracy proxy: {accuracy}")
    print(f"CSV: {OUT}")
    print(f"Report: {REPORT}")


if __name__ == "__main__":
    main()
