from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

DATA = Path("data/training_dataset_family_provider_v1.csv")
TRAIN = Path("data/train_dataset_v1.csv")
VALID = Path("data/validation_dataset_v1.csv")

OUT = Path("data/random_forest_model_v1.csv")
REPORT = Path("reports/random_forest_model_v1.md")

CATEGORICAL = ["provider_family", "gpu_family", "market_regime"]
NUMERIC = [
    "record_count",
    "avg_price",
    "price_spread",
    "availability_sum",
    "historical_gpu_release_count",
    "historical_market_event_count",
]


def read(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size <= 1:
        raise SystemExit(f"Missing dataset: {path}")
    return pd.read_csv(path)


def split_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    train_count = len(read(TRAIN))
    valid_count = len(read(VALID))

    train = df.iloc[:train_count].copy()
    validation = df.iloc[train_count:train_count + valid_count].copy()
    test = df.iloc[train_count + valid_count:].copy()

    return train, validation, test


def prepare(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()

    for col in CATEGORICAL:
        if col not in data.columns:
            data[col] = "unknown"
        data[col] = data[col].fillna("unknown").astype(str)

    for col in NUMERIC:
        if col not in data.columns:
            data[col] = 0
        data[col] = pd.to_numeric(data[col], errors="coerce").fillna(0)

    return data


def evaluate(model: Pipeline, df: pd.DataFrame, split: str) -> pd.DataFrame:
    X = df[CATEGORICAL + NUMERIC]
    y = df["future_market_regime"].fillna("unknown").astype(str)

    pred = model.predict(X)

    out = df[["provider", "gpu", "provider_family", "gpu_family", "future_market_regime"]].copy()
    out["model_name"] = "random_forest_model_v1"
    out["predicted_market_regime"] = pred
    out["prediction_correct"] = pred == y
    out["evaluation_split"] = split

    return out


def main() -> None:
    df = prepare(read(DATA))

    if "future_market_regime" not in df.columns:
        raise SystemExit("future_market_regime missing")

    train, validation, test = split_data(df)

    X_train = train[CATEGORICAL + NUMERIC]
    y_train = train["future_market_regime"].fillna("unknown").astype(str)

    model = Pipeline(
        steps=[
            (
                "preprocess",
                ColumnTransformer(
                    transformers=[
                        ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),
                        ("num", "passthrough", NUMERIC),
                    ]
                ),
            ),
            (
                "rf",
                RandomForestClassifier(
                    n_estimators=100,
                    max_depth=5,
                    random_state=42,
                    class_weight="balanced",
                ),
            ),
        ]
    )

    model.fit(X_train, y_train)

    result = pd.concat(
        [
            evaluate(model, train, "train"),
            evaluate(model, validation, "validation"),
            evaluate(model, test, "test"),
        ],
        ignore_index=True,
        sort=False,
    )

    summary = (
        result.groupby("evaluation_split")["prediction_correct"]
        .mean()
        .mul(100)
        .round(2)
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    result.to_csv(OUT, index=False)

    REPORT.write_text(
        "\n".join(
            [
                "# Random Forest Model v1",
                "",
                f"Train Accuracy: {summary.get('train', 0)}%",
                f"Validation Accuracy: {summary.get('validation', 0)}%",
                f"Test Accuracy: {summary.get('test', 0)}%",
                "",
                "## Features",
                "",
                "- provider_family",
                "- gpu_family",
                "- market_regime",
                "- record_count",
                "- avg_price",
                "- price_spread",
                "- availability_sum",
                "- historical context counts",
                "",
                "## CTO Assessment",
                "",
                "This is the first true ML classifier benchmarked against Forecast Engine v8.",
                "It should be compared on validation and test accuracy before any production claim.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print("RANDOM FOREST MODEL V1")
    print("======================")
    print(summary)
    print(f"Rows: {len(result)}")
    print(f"CSV: {OUT}")


if __name__ == "__main__":
    main()
