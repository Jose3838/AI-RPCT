from __future__ import annotations

from pathlib import Path

import pandas as pd

TRAINING = Path("data/training_dataset_v1.csv")

TRAIN_OUT = Path("data/train_dataset_v1.csv")
VALID_OUT = Path("data/validation_dataset_v1.csv")
TEST_OUT = Path("data/test_dataset_v1.csv")

REPORT = Path("reports/training_split_engine_v1.md")


def main() -> None:

    if not TRAINING.exists():
        raise SystemExit("training_dataset_v1.csv missing")

    df = pd.read_csv(TRAINING)

    if df.empty:
        raise SystemExit("training dataset empty")

    # Zeitlich sortieren, falls vorhanden
    if "latest_timestamp" in df.columns:
        df = df.sort_values("latest_timestamp")

    total = len(df)

    train_end = int(total * 0.70)
    valid_end = int(total * 0.85)

    train = df.iloc[:train_end].copy()
    validation = df.iloc[train_end:valid_end].copy()
    test = df.iloc[valid_end:].copy()

    train["dataset_split"] = "train"
    validation["dataset_split"] = "validation"
    test["dataset_split"] = "test"

    TRAIN_OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    train.to_csv(TRAIN_OUT, index=False)
    validation.to_csv(VALID_OUT, index=False)
    test.to_csv(TEST_OUT, index=False)

    REPORT.write_text(
        "\n".join(
            [
                "# Training Split Engine v1",
                "",
                f"Total rows: {total}",
                f"Train rows: {len(train)}",
                f"Validation rows: {len(validation)}",
                f"Test rows: {len(test)}",
                "",
                "## Split Strategy",
                "",
                "70% Train",
                "15% Validation",
                "15% Test",
                "",
                "The split is chronological when timestamps are available.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print("TRAINING SPLIT ENGINE V1")
    print("========================")
    print(f"Train      : {len(train)}")
    print(f"Validation : {len(validation)}")
    print(f"Test       : {len(test)}")
    print(f"Total      : {total}")


if __name__ == "__main__":
    main()
