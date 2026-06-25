from __future__ import annotations

from pathlib import Path

import pandas as pd

LEAKAGE = Path("data/leakage_audit_v2.csv")
TRAINING = Path("data/training_dataset_v3_readiness.csv")
RETRAINING = Path("data/auto_retraining_manager_v1.csv")
CUSTOMER = Path("data/customer_forecast_readiness_v1.csv")
BENCHMARK = Path("data/model_benchmark_v1.csv")

OUT = Path("data/production_promotion_guard_v1.csv")
REPORT = Path("reports/production_promotion_guard_v1.md")


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size <= 1:
        return pd.DataFrame()
    return pd.read_csv(path)


def bool_value(value) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def main() -> None:
    leakage = read_csv(LEAKAGE)
    training = read_csv(TRAINING)
    retraining = read_csv(RETRAINING)
    customer = read_csv(CUSTOMER)
    benchmark = read_csv(BENCHMARK)

    blockers = []

    leakage_block = False
    if not leakage.empty and "production_block" in leakage.columns:
        leakage_block = leakage["production_block"].fillna(False).apply(bool_value).any()
    if leakage.empty:
        blockers.append("missing_leakage_audit")
    elif leakage_block:
        blockers.append("leakage_audit_block")

    training_status = "missing"
    training_rows = 0
    trainable_labels = 0

    if training.empty:
        blockers.append("missing_training_dataset_v3_readiness")
    else:
        training_status = str(training.iloc[0].get("status", "unknown"))
        training_rows = int(training.iloc[0].get("training_rows", 0))
        trainable_labels = int(training.iloc[0].get("trainable_label_rows", 0))

        if training_status != "ready":
            blockers.append("training_dataset_v3_not_ready")
        if training_rows <= 0:
            blockers.append("no_true_outcome_training_rows")
        if trainable_labels <= 0:
            blockers.append("no_trainable_true_labels")

    retraining_allowed = False
    if retraining.empty:
        blockers.append("missing_auto_retraining_manager")
    else:
        retraining_allowed = bool_value(retraining.iloc[0].get("retraining_allowed", False))
        if not retraining_allowed:
            blockers.append("auto_retraining_not_allowed")

    customer_preview_ready = False
    paid_production_ready = False

    if customer.empty:
        blockers.append("missing_customer_forecast_readiness")
    else:
        customer_preview_ready = bool_value(customer.iloc[0].get("customer_preview_ready", False))
        paid_production_ready = bool_value(customer.iloc[0].get("paid_production_ready", False))

        if not customer_preview_ready:
            blockers.append("customer_preview_not_ready")
        if not paid_production_ready:
            blockers.append("paid_production_not_ready")

    if benchmark.empty:
        blockers.append("missing_model_benchmark")

    promotion_allowed = len(blockers) == 0

    if promotion_allowed:
        status = "promotion_allowed"
        next_action = "Promote champion model to production."
    elif "no_trainable_true_labels" in blockers:
        status = "blocked_waiting_for_true_labels"
        next_action = "Continue collecting forecasts until outcome windows mature and true labels resolve."
    elif "leakage_audit_block" in blockers:
        status = "blocked_by_leakage_audit"
        next_action = "Fix leakage issues and rebuild training data."
    else:
        status = "blocked"
        next_action = "Resolve promotion blockers before production promotion."

    row = {
        "guard": "production_promotion_guard_v1",
        "promotion_allowed": promotion_allowed,
        "status": status,
        "training_status": training_status,
        "training_rows": training_rows,
        "trainable_labels": trainable_labels,
        "retraining_allowed": retraining_allowed,
        "customer_preview_ready": customer_preview_ready,
        "paid_production_ready": paid_production_ready,
        "blockers": ", ".join(blockers) if blockers else "none",
        "next_action": next_action,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    pd.DataFrame([row]).to_csv(OUT, index=False)

    REPORT.write_text(
        "\n".join([
            "# Production Promotion Guard v1",
            "",
            f"Promotion allowed: {promotion_allowed}",
            f"Status: {status}",
            f"Training rows: {training_rows}",
            f"Trainable labels: {trainable_labels}",
            "",
            "## Blockers",
            "",
            row["blockers"],
            "",
            "## Next Action",
            "",
            next_action,
            "",
            "## CTO Assessment",
            "",
            "This guard prevents model promotion until leakage checks, true outcome labels, retraining readiness, customer readiness, and benchmark evidence are all aligned.",
            "The correct current state is expected to be blocked until true future labels mature.",
            "",
        ]),
        encoding="utf-8",
    )

    print("PRODUCTION PROMOTION GUARD V1")
    print("=============================")
    print(pd.DataFrame([row]))


if __name__ == "__main__":
    main()
