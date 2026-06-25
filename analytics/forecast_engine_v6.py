from __future__ import annotations

from pathlib import Path

import pandas as pd

TRAIN = Path("data/train_dataset_v1.csv")
VALIDATION = Path("data/validation_dataset_v1.csv")
TEST = Path("data/test_dataset_v1.csv")

OUT = Path("data/forecast_engine_v6.csv")
REPORT = Path("reports/forecast_engine_v6.md")


def read(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size <= 1:
        return pd.DataFrame()
    return pd.read_csv(path)


def build_baseline(train: pd.DataFrame) -> pd.DataFrame:
    grouped = (
        train.groupby(["provider", "gpu"])["future_market_regime"]
        .agg(lambda s: s.dropna().mode().iloc[0] if not s.dropna().empty else "unknown")
        .reset_index()
        .rename(columns={"future_market_regime": "predicted_market_regime"})
    )
    return grouped


def score_dataset(dataset: pd.DataFrame, model: pd.DataFrame, split: str) -> pd.DataFrame:
    merged = dataset.merge(
        model,
        on=["provider", "gpu"],
        how="left",
    )

    merged["predicted_market_regime"] = (
        merged["predicted_market_regime"]
        .fillna("unknown")
    )

    merged["prediction_correct"] = (
        merged["predicted_market_regime"]
        == merged["future_market_regime"]
    )

    merged["evaluation_split"] = split

    return merged


def main() -> None:
    train = read(TRAIN)
    validation = read(VALIDATION)
    test = read(TEST)

    if train.empty:
        raise SystemExit("train_dataset_v1.csv missing")

    model = build_baseline(train)

    train_eval = score_dataset(train, model, "train")
    valid_eval = score_dataset(validation, model, "validation")
    test_eval = score_dataset(test, model, "test")

    result = pd.concat(
        [train_eval, valid_eval, test_eval],
        ignore_index=True,
        sort=False,
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    result.to_csv(OUT, index=False)

    summary = (
        result.groupby("evaluation_split")["prediction_correct"]
        .mean()
        .fillna(0)
        .mul(100)
        .round(2)
    )

    REPORT.write_text(
        "\n".join(
            [
                "# Forecast Engine v6",
                "",
                "## Accuracy",
                "",
                f"Train: {summary.get('train', 0)}%",
                f"Validation: {summary.get('validation', 0)}%",
                f"Test: {summary.get('test', 0)}%",
                "",
                "## CTO Assessment",
                "",
                "Forecast Engine v6 is the first engine evaluated on separate train, validation, and test datasets.",
                "Future versions should replace the baseline learner with more advanced ML models while keeping this evaluation pipeline.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print("FORECAST ENGINE V6")
    print("==================")
    print(summary)
    print(f"Rows: {len(result)}")
    print(f"CSV: {OUT}")


if __name__ == "__main__":
    main()
