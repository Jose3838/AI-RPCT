from __future__ import annotations

from pathlib import Path

import pandas as pd

FORECAST = Path("data/forecast_engine_v8.csv")

OUT = Path("data/ml_evaluation_guard_v2.csv")
REPORT = Path("reports/ml_evaluation_guard_v2.md")


def main() -> None:
    if not FORECAST.exists():
        raise SystemExit("forecast_engine_v8.csv not found")

    df = pd.read_csv(FORECAST)

    summary = (
        df.groupby("evaluation_split")["prediction_correct"]
        .mean()
        .mul(100)
        .round(2)
    )

    train = float(summary.get("train", 0))
    validation = float(summary.get("validation", 0))
    test = float(summary.get("test", 0))

    gap = round(abs(train - validation), 2)

    if validation >= 85 and test >= 85 and gap <= 10:
        status = "production_ready"
        reason = "Strong validation and test performance."
    elif validation >= 60 and test >= 60:
        status = "watch"
        reason = "Generalization improved, but dataset is still limited."
    else:
        status = "blocked"
        reason = "Model does not generalize sufficiently."

    row = {
        "model_name": "forecast_engine_v8",
        "train_accuracy": train,
        "validation_accuracy": validation,
        "test_accuracy": test,
        "generalization_gap": gap,
        "status": status,
        "reason": reason,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    pd.DataFrame([row]).to_csv(OUT, index=False)

    REPORT.write_text(
        "\n".join(
            [
                "# ML Evaluation Guard v2",
                "",
                f"Train Accuracy: {train}%",
                f"Validation Accuracy: {validation}%",
                f"Test Accuracy: {test}%",
                f"Generalization Gap: {gap}%",
                "",
                f"Status: {status}",
                "",
                "## Assessment",
                "",
                reason,
                "",
                "Recommendation:",
                "- Continue collecting live data.",
                "- Increase historical provider coverage.",
                "- Benchmark against tree-based ML models.",
            ]
        ),
        encoding="utf-8",
    )

    print("ML EVALUATION GUARD V2")
    print("======================")
    print(pd.DataFrame([row]))


if __name__ == "__main__":
    main()
