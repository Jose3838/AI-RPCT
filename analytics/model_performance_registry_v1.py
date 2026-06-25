from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

BACKTEST = Path("data/forecast_backtest_v1.csv")
OUT = Path("data/model_performance_registry_v1.csv")
REPORT = Path("reports/model_performance_registry_v1.md")


def main():

    if not BACKTEST.exists():
        raise SystemExit("forecast_backtest_v1.csv missing")

    df = pd.read_csv(BACKTEST)

    total = len(df)

    correct = int(
        (df["backtest_result"] == "directionally_correct").sum()
    )

    validation = int(
        (df["backtest_result"] == "needs_future_validation").sum()
    )

    pending = int(
        (df["backtest_result"] == "not_evaluable").sum()
    )

    accuracy = round(correct / total, 4) if total else 0

    registry = pd.DataFrame([
        {
            "timestamp": datetime.now(UTC).isoformat(),
            "model_name": "forecast_engine_v1",
            "model_version": "1.0",
            "forecast_rows": total,
            "directionally_correct": correct,
            "pending_validation": validation,
            "not_evaluable": pending,
            "directional_accuracy": accuracy,
            "status": "active"
        }
    ])

    OUT.parent.mkdir(exist_ok=True)
    REPORT.parent.mkdir(exist_ok=True)

    registry.to_csv(OUT, index=False)

    REPORT.write_text(
f"""# Model Performance Registry

Model: Forecast Engine v1

Forecast rows: {total}

Directional accuracy: {accuracy}

Current status:
Active

Future versions of AI-RPCT will compare multiple model versions
and automatically determine which forecast engine performs best.
""",
encoding="utf-8"
)

    print("MODEL PERFORMANCE REGISTRY")
    print("==========================")
    print(registry)

if __name__ == "__main__":
    main()
