from __future__ import annotations

from pathlib import Path

import pandas as pd

GUARD = Path("data/ml_evaluation_guard_v1.csv")
TRAINING = Path("data/training_dataset_v1.csv")
V6 = Path("data/forecast_engine_v6.csv")

OUT = Path("data/feature_generalization_plan_v1.csv")
REPORT = Path("reports/feature_generalization_plan_v1.md")


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size <= 1:
        return pd.DataFrame()
    return pd.read_csv(path)


def main() -> None:
    guard = read_csv(GUARD)
    training = read_csv(TRAINING)
    v6 = read_csv(V6)

    rows = []

    validation_accuracy = 0.0
    test_accuracy = 0.0

    if not guard.empty:
        validation_accuracy = float(guard.iloc[0].get("validation_accuracy", 0))
        test_accuracy = float(guard.iloc[0].get("test_accuracy", 0))

    provider_count = training["provider"].nunique() if "provider" in training.columns else 0
    gpu_count = training["gpu"].nunique() if "gpu" in training.columns else 0
    row_count = len(training)

    avg_rows_per_gpu = round(row_count / gpu_count, 2) if gpu_count else 0

    if validation_accuracy < 50:
        rows.append({
            "priority": "critical",
            "gap": "poor_validation_generalization",
            "evidence": f"validation_accuracy={validation_accuracy}",
            "recommended_action": "Group sparse GPU variants into normalized GPU families before training.",
            "business_reason": "Reduces overfitting and improves forecast transfer across similar GPUs.",
        })

    if test_accuracy < 50:
        rows.append({
            "priority": "critical",
            "gap": "poor_test_generalization",
            "evidence": f"test_accuracy={test_accuracy}",
            "recommended_action": "Increase historical and live samples before allowing ML-backed production claims.",
            "business_reason": "Prevents unreliable forecasts from being sold as decision intelligence.",
        })

    if avg_rows_per_gpu < 10:
        rows.append({
            "priority": "high",
            "gap": "sparse_gpu_history",
            "evidence": f"avg_rows_per_gpu={avg_rows_per_gpu}",
            "recommended_action": "Create GPU family normalization: H100/H200/B200/A100/RTX40/RTX50/Legacy.",
            "business_reason": "Transforms thin individual series into broader learnable market segments.",
        })

    if provider_count < 5:
        rows.append({
            "priority": "high",
            "gap": "limited_provider_diversity",
            "evidence": f"provider_count={provider_count}",
            "recommended_action": "Add historical provider coverage for AWS, Azure, GCP, CoreWeave, Lambda, Crusoe, Nebius.",
            "business_reason": "Improves market representativeness and enterprise credibility.",
        })

    if "price_per_hour" not in training.columns or pd.to_numeric(training.get("price_per_hour"), errors="coerce").fillna(0).sum() == 0:
        rows.append({
            "priority": "high",
            "gap": "weak_price_signal",
            "evidence": "price_per_hour missing_or_zero",
            "recommended_action": "Prioritize real historical price sources and normalize price basis: on-demand, spot, reserved.",
            "business_reason": "Price forecasting is commercially valuable only with trusted price signals.",
        })

    if not v6.empty:
        unseen = v6[(v6["evaluation_split"].isin(["validation", "test"])) & (v6["predicted_market_regime"] == "unknown")]
        if len(unseen) > 0:
            rows.append({
                "priority": "medium",
                "gap": "unseen_provider_gpu_pairs",
                "evidence": f"unknown_predictions={len(unseen)}",
                "recommended_action": "Train models at provider-family and GPU-family level, not only exact provider/GPU pair.",
                "business_reason": "Allows forecasts for newly observed GPUs and providers.",
            })

    if not rows:
        rows.append({
            "priority": "low",
            "gap": "no_major_generalization_gap_detected",
            "evidence": "guard_ok",
            "recommended_action": "Proceed to ML model v1.",
            "business_reason": "Model is ready for next-stage evaluation.",
        })

    out = pd.DataFrame(rows)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    out.to_csv(OUT, index=False)

    REPORT.write_text(
        "\n".join([
            "# Feature Generalization Plan v1",
            "",
            f"Training rows: {row_count}",
            f"Providers: {provider_count}",
            f"GPUs: {gpu_count}",
            f"Avg rows per GPU: {avg_rows_per_gpu}",
            f"Validation accuracy: {validation_accuracy}",
            f"Test accuracy: {test_accuracy}",
            "",
            "## CTO Assessment",
            "",
            "Forecast Engine v6 proves the ML pipeline exists, but the model does not yet generalize.",
            "The next step is not a more complex model; it is better feature generalization and richer historical data.",
            "",
            "## Recommended Focus",
            "",
            "1. GPU family normalization",
            "2. Provider family normalization",
            "3. Real historical price basis",
            "4. More provider diversity",
            "5. More outcome history",
            "",
        ]),
        encoding="utf-8",
    )

    print("FEATURE GENERALIZATION PLAN V1")
    print("==============================")
    print(out)


if __name__ == "__main__":
    main()
