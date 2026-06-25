from __future__ import annotations

from pathlib import Path

import pandas as pd

FEATURES = Path("data/feature_store_v2.csv")
LABELS = Path("data/true_outcome_labels_v1.csv")

OUT = Path("data/training_dataset_v3.csv")
READINESS = Path("data/training_dataset_v3_readiness.csv")
REPORT = Path("reports/training_dataset_builder_v3.md")


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size <= 1:
        return pd.DataFrame()
    return pd.read_csv(path)


def as_bool(value) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def main() -> None:
    features = read_csv(FEATURES)
    labels = read_csv(LABELS)

    if features.empty:
        raise SystemExit("feature_store_v2.csv missing or empty")

    if labels.empty:
        trainable = pd.DataFrame()
    else:
        labels["is_trainable_bool"] = labels["is_trainable"].apply(as_bool)
        trainable = labels[
            labels["is_trainable_bool"]
            & labels["true_outcome_label"].fillna("").astype(str).str.len().gt(0)
        ].copy()

    if trainable.empty:
        dataset = pd.DataFrame(columns=list(features.columns) + ["true_outcome_label"])
        status = "not_ready"
        reason = "No trainable true future outcome labels are available yet."
    else:
        dataset = features.merge(
            trainable[
                [
                    "provider",
                    "gpu",
                    "window_days",
                    "true_outcome_label",
                    "label_status",
                    "label_source",
                ]
            ],
            on=["provider", "gpu"],
            how="inner",
        )
        status = "ready" if not dataset.empty else "not_ready"
        reason = "Training dataset built from true future outcome labels."

    readiness = {
        "training_dataset": "training_dataset_v3",
        "status": status,
        "feature_rows": len(features),
        "true_label_rows": len(labels),
        "trainable_label_rows": len(trainable),
        "training_rows": len(dataset),
        "reason": reason,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    READINESS.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    dataset.to_csv(OUT, index=False)
    pd.DataFrame([readiness]).to_csv(READINESS, index=False)

    REPORT.write_text(
        "\n".join([
            "# Training Dataset Builder v3",
            "",
            f"Status: {status}",
            f"Feature rows: {len(features)}",
            f"True label rows: {len(labels)}",
            f"Trainable label rows: {len(trainable)}",
            f"Training rows: {len(dataset)}",
            "",
            "## CTO Assessment",
            "",
            "Training Dataset v3 only allows true future outcome labels as model targets.",
            "This prevents current-state market regimes from being used as fake predictive labels.",
            "",
            "## Reason",
            "",
            reason,
            "",
        ]),
        encoding="utf-8",
    )

    print("TRAINING DATASET BUILDER V3")
    print("===========================")
    print(pd.DataFrame([readiness]))
    print(f"CSV: {OUT}")
    print(f"Readiness: {READINESS}")


if __name__ == "__main__":
    main()
