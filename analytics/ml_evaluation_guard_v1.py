from __future__ import annotations

from pathlib import Path

import pandas as pd

FORECAST_V6 = Path("data/forecast_engine_v6.csv")
OUT = Path("data/ml_evaluation_guard_v1.csv")
REPORT = Path("reports/ml_evaluation_guard_v1.md")


def split_accuracy(df: pd.DataFrame, split: str) -> float:
    subset = df[df["evaluation_split"] == split]
    if subset.empty:
        return 0.0
    return round(float(subset["prediction_correct"].mean() * 100), 2)


def main() -> None:
    if not FORECAST_V6.exists() or FORECAST_V6.stat().st_size <= 1:
        raise SystemExit("forecast_engine_v6.csv missing or empty")

    df = pd.read_csv(FORECAST_V6)

    train_accuracy = split_accuracy(df, "train")
    validation_accuracy = split_accuracy(df, "validation")
    test_accuracy = split_accuracy(df, "test")

    generalization_gap = round(train_accuracy - validation_accuracy, 2)

    blockers = []

    if validation_accuracy < 50:
        blockers.append("poor_validation_generalization")

    if test_accuracy < 50:
        blockers.append("poor_test_generalization")

    if generalization_gap > 30:
        blockers.append("large_train_validation_gap")

    production_ready = len(blockers) == 0

    row = {
        "model_name": "forecast_engine_v6",
        "train_accuracy": train_accuracy,
        "validation_accuracy": validation_accuracy,
        "test_accuracy": test_accuracy,
        "generalization_gap": generalization_gap,
        "production_ready": production_ready,
        "blockers": ", ".join(blockers) if blockers else "none",
        "next_action": (
            "Collect more live history and improve feature generalization."
            if blockers
            else "Eligible for champion/challenger promotion."
        ),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    pd.DataFrame([row]).to_csv(OUT, index=False)

    REPORT.write_text(
        "\n".join(
            [
                "# ML Evaluation Guard v1",
                "",
                f"Model: {row['model_name']}",
                f"Train accuracy: {train_accuracy}%",
                f"Validation accuracy: {validation_accuracy}%",
                f"Test accuracy: {test_accuracy}%",
                f"Generalization gap: {generalization_gap}%",
                f"Production ready: {production_ready}",
                f"Blockers: {row['blockers']}",
                "",
                "## CTO Assessment",
                "",
                "This guard prevents overfit or poorly generalizing models from being presented as production-ready.",
                "Forecast Engine v6 currently demonstrates ML pipeline readiness, but not yet reliable predictive performance.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print("ML EVALUATION GUARD V1")
    print("======================")
    print(pd.DataFrame([row]))


if __name__ == "__main__":
    main()
