from __future__ import annotations

from pathlib import Path

import pandas as pd

DATA = Path("data/training_dataset_family_provider_v1.csv")
TRAIN = Path("data/train_dataset_v1.csv")
VALID = Path("data/validation_dataset_v1.csv")

OUT = Path("data/forecast_engine_v8.csv")
REPORT = Path("reports/forecast_engine_v8.md")


def read(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size <= 1:
        raise SystemExit(f"Missing dataset: {path}")
    return pd.read_csv(path)


def evaluate(split_df: pd.DataFrame, model: pd.DataFrame, split_name: str) -> pd.DataFrame:
    merged = split_df.merge(
        model,
        on=["provider_family", "gpu_family"],
        how="left",
    )

    merged["predicted_market_regime"] = merged["predicted_market_regime"].fillna("unknown")
    merged["prediction_correct"] = merged["predicted_market_regime"] == merged["future_market_regime"]
    merged["evaluation_split"] = split_name

    return merged


def main() -> None:
    data = read(DATA)

    train_count = len(read(TRAIN))
    valid_count = len(read(VALID))

    train = data.iloc[:train_count].copy()
    validation = data.iloc[train_count:train_count + valid_count].copy()
    test = data.iloc[train_count + valid_count:].copy()

    model = (
        train.groupby(["provider_family", "gpu_family"])["future_market_regime"]
        .agg(lambda x: x.mode().iloc[0] if not x.mode().empty else "unknown")
        .reset_index()
        .rename(columns={"future_market_regime": "predicted_market_regime"})
    )

    result = pd.concat(
        [
            evaluate(train, model, "train"),
            evaluate(validation, model, "validation"),
            evaluate(test, model, "test"),
        ],
        ignore_index=True,
        sort=False,
    )

    summary = (
        result.groupby("evaluation_split")["prediction_correct"]
        .mean()
        .fillna(0)
        .mul(100)
        .round(2)
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    result.to_csv(OUT, index=False)

    REPORT.write_text(
        "\n".join(
            [
                "# Forecast Engine v8",
                "",
                f"Train Accuracy: {summary.get('train', 0)}%",
                f"Validation Accuracy: {summary.get('validation', 0)}%",
                f"Test Accuracy: {summary.get('test', 0)}%",
                "",
                "## CTO Assessment",
                "",
                "Forecast Engine v8 learns from provider_family + gpu_family instead of exact provider/GPU pairs.",
                "This tests whether structural grouping improves generalization on sparse data.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print("FORECAST ENGINE V8")
    print("==================")
    print(summary)
    print(f"Rows: {len(result)}")
    print(f"CSV: {OUT}")


if __name__ == "__main__":
    main()
