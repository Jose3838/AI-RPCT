from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

DATA = Path("data/training_dataset_v2.csv")

OUT = Path("data/gradient_boosting_model_v1.csv")
REPORT = Path("reports/gradient_boosting_model_v1.md")

CATEGORICAL = [
    "provider_family",
    "gpu_family",
    "market_regime",
    "forecast_signal",
]

NUMERIC = [
    "record_count",
    "avg_price",
    "min_price",
    "max_price",
    "price_spread",
    "availability_sum",
    "confidence",
    "historical_gpu_release_count",
    "historical_market_event_count",
    "historical_family_rows",
    "historical_provider_count",
    "historical_gpu_family_count",
    "forecast_score",
]


def read_data() -> pd.DataFrame:
    if not DATA.exists() or DATA.stat().st_size <= 1:
        raise SystemExit("training_dataset_v2.csv missing or empty")
    return pd.read_csv(DATA)


def prepare(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()

    if "future_market_regime" not in data.columns:
        if "market_regime" in data.columns:
            data["future_market_regime"] = data["market_regime"]
        else:
            raise SystemExit("No target column available")

    for col in CATEGORICAL:
        if col not in data.columns:
            data[col] = "unknown"
        data[col] = data[col].fillna("unknown").astype(str)

    for col in NUMERIC:
        if col not in data.columns:
            data[col] = 0
        data[col] = pd.to_numeric(data[col], errors="coerce").fillna(0)

    return data


def split_data(df: pd.DataFrame):
    if "latest_timestamp" in df.columns:
        df = df.sort_values("latest_timestamp")

    total = len(df)
    train_end = int(total * 0.70)
    valid_end = int(total * 0.85)

    return (
        df.iloc[:train_end].copy(),
        df.iloc[train_end:valid_end].copy(),
        df.iloc[valid_end:].copy(),
    )


def evaluate(model: Pipeline, df: pd.DataFrame, split: str) -> pd.DataFrame:
    X = df[CATEGORICAL + NUMERIC]
    y = df["future_market_regime"].fillna("unknown").astype(str)
    pred = model.predict(X)

    out = df[["provider", "gpu", "provider_family", "gpu_family", "future_market_regime"]].copy()
    out["model_name"] = "gradient_boosting_model_v1"
    out["predicted_market_regime"] = pred
    out["prediction_correct"] = pred == y
    out["evaluation_split"] = split
    return out


def main() -> None:
    df = prepare(read_data())
    train, validation, test = split_data(df)

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
                "gb",
                GradientBoostingClassifier(
                    n_estimators=100,
                    learning_rate=0.05,
                    max_depth=3,
                    random_state=42,
                ),
            ),
        ]
    )

    X_train = train[CATEGORICAL + NUMERIC]
    y_train = train["future_market_regime"].fillna("unknown").astype(str)

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
                "# Gradient Boosting Model v1",
                "",
                f"Train Accuracy: {summary.get('train', 0)}%",
                f"Validation Accuracy: {summary.get('validation', 0)}%",
                f"Test Accuracy: {summary.get('test', 0)}%",
                "",
                "## CTO Assessment",
                "",
                "This is the first gradient boosting benchmark on Training Dataset v2.",
                "It must be compared against Forecast Engine v9 and prior ML baselines before any production promotion.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print("GRADIENT BOOSTING MODEL V1")
    print("==========================")
    print(summary)
    print(f"Rows: {len(result)}")
    print(f"CSV: {OUT}")


if __name__ == "__main__":
    main()
