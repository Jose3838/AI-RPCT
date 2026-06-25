from __future__ import annotations

from pathlib import Path

import pandas as pd

CUSTOMER = Path("data/customer_forecast_readiness_v1.csv")
PROMOTION = Path("data/production_promotion_guard_v1.csv")
RETRAINING = Path("data/auto_retraining_manager_v1.csv")
TRAINING = Path("data/training_dataset_v3_readiness.csv")
RESOLVER = Path("data/true_outcome_resolver_summary_v1.csv")

OUT = Path("data/ai_rpct_readiness_dashboard_v1.csv")
REPORT = Path("reports/ai_rpct_readiness_dashboard_v1.md")


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size <= 1:
        return pd.DataFrame()
    return pd.read_csv(path)


def as_bool(value) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def main() -> None:
    customer = read_csv(CUSTOMER)
    promotion = read_csv(PROMOTION)
    retraining = read_csv(RETRAINING)
    training = read_csv(TRAINING)
    resolver = read_csv(RESOLVER)

    preview_ready = False
    paid_ready = False
    promotion_allowed = False
    retraining_allowed = False
    training_status = "unknown"
    trainable_labels = 0
    resolved_labels = 0

    if not customer.empty:
        preview_ready = as_bool(customer.iloc[0]["customer_preview_ready"])
        paid_ready = as_bool(customer.iloc[0]["paid_production_ready"])

    if not promotion.empty:
        promotion_allowed = as_bool(promotion.iloc[0]["promotion_allowed"])

    if not retraining.empty:
        retraining_allowed = as_bool(retraining.iloc[0]["retraining_allowed"])

    if not training.empty:
        training_status = str(training.iloc[0]["status"])
        trainable_labels = int(training.iloc[0]["trainable_label_rows"])

    if not resolver.empty:
        resolved_labels = int(resolver.iloc[0]["resolved_labels"])

    if promotion_allowed:
        stage = "production"
    elif preview_ready:
        stage = "pilot"
    else:
        stage = "development"

    row = {
        "platform": "AI-RPCT",
        "platform_stage": stage,
        "customer_demo_allowed": preview_ready,
        "paid_production_allowed": paid_ready,
        "production_promotion_allowed": promotion_allowed,
        "ml_retraining_allowed": retraining_allowed,
        "training_dataset_status": training_status,
        "resolved_true_labels": resolved_labels,
        "trainable_true_labels": trainable_labels,
        "next_milestone": (
            "Collect mature true outcome labels"
            if trainable_labels == 0
            else "Retrain ML models"
        ),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    pd.DataFrame([row]).to_csv(OUT, index=False)

    REPORT.write_text(
        "\n".join([
            "# AI-RPCT Readiness Dashboard v1",
            "",
            f"Platform stage: {stage}",
            f"Customer demo allowed: {preview_ready}",
            f"Paid production allowed: {paid_ready}",
            f"ML retraining allowed: {retraining_allowed}",
            f"Trainable labels: {trainable_labels}",
            "",
            "## CTO Assessment",
            "",
            "This dashboard summarizes the operational readiness of the AI-RPCT forecasting platform.",
            "It provides a single governance view for engineering, product, and customer communication.",
            "",
        ]),
        encoding="utf-8",
    )

    print("AI-RPCT READINESS DASHBOARD V1")
    print("==============================")
    print(pd.DataFrame([row]))


if __name__ == "__main__":
    main()
