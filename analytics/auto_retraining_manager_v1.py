from __future__ import annotations

from pathlib import Path

import pandas as pd

READINESS = Path("data/training_dataset_v3_readiness.csv")
RESOLVER = Path("data/true_outcome_resolver_summary_v1.csv")

OUT = Path("data/auto_retraining_manager_v1.csv")
REPORT = Path("reports/auto_retraining_manager_v1.md")

MIN_TRAINABLE_LABELS = 100


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size <= 1:
        return pd.DataFrame()
    return pd.read_csv(path)


def main() -> None:
    readiness = read_csv(READINESS)
    resolver = read_csv(RESOLVER)

    trainable_labels = 0
    training_rows = 0

    if not readiness.empty:
        trainable_labels = int(readiness.iloc[0].get("trainable_label_rows", 0))
        training_rows = int(readiness.iloc[0].get("training_rows", 0))

    if not resolver.empty:
        trainable_labels = max(
            trainable_labels,
            int(resolver.iloc[0].get("trainable_labels", 0)),
        )

    retraining_allowed = (
        trainable_labels >= MIN_TRAINABLE_LABELS
        and training_rows >= MIN_TRAINABLE_LABELS
    )

    row = {
        "manager": "auto_retraining_manager_v1",
        "min_trainable_labels": MIN_TRAINABLE_LABELS,
        "trainable_labels": trainable_labels,
        "training_rows": training_rows,
        "retraining_allowed": retraining_allowed,
        "status": "ready" if retraining_allowed else "waiting_for_labels",
        "next_action": (
            "Run ML retraining and benchmark candidates."
            if retraining_allowed
            else "Continue collecting forecasts and resolving matured outcomes."
        ),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    pd.DataFrame([row]).to_csv(OUT, index=False)

    REPORT.write_text(
        "\n".join([
            "# Auto Retraining Manager v1",
            "",
            f"Minimum trainable labels: {MIN_TRAINABLE_LABELS}",
            f"Trainable labels: {trainable_labels}",
            f"Training rows: {training_rows}",
            f"Retraining allowed: {retraining_allowed}",
            "",
            "## CTO Assessment",
            "",
            "This manager prevents automatic retraining until enough true future outcome labels exist.",
            "It protects the ML pipeline from retraining on immature, proxy, or leaked labels.",
            "",
        ]),
        encoding="utf-8",
    )

    print("AUTO RETRAINING MANAGER V1")
    print("==========================")
    print(pd.DataFrame([row]))


if __name__ == "__main__":
    main()
