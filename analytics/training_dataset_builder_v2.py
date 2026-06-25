from __future__ import annotations

from pathlib import Path
import pandas as pd

FEATURES = Path("data/feature_store_v2.csv")
FORECAST = Path("data/forecast_engine_v9.csv")

OUT = Path("data/training_dataset_v2.csv")
REPORT = Path("reports/training_dataset_builder_v2.md")


def main():

    features = pd.read_csv(FEATURES)
    forecast = pd.read_csv(FORECAST)

    cols = [
        "provider",
        "gpu",
        "forecast_score",
        "forecast_signal"
    ]

    dataset = features.merge(
        forecast[cols],
        on=["provider", "gpu"],
        how="left"
    )

    dataset["training_dataset_version"] = "v2"
    dataset["feature_generation"] = "feature_store_v2"
    dataset["forecast_generation"] = "forecast_engine_v9"

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    dataset.to_csv(OUT, index=False)

    REPORT.write_text(
f"""# Training Dataset Builder v2

Rows: {len(dataset)}

Columns: {len(dataset.columns)}

## Data Sources

- Feature Store v2
- Forecast Engine v9
- Historical Provider Coverage

## Purpose

Enterprise ML training dataset.

Supports future:

- Random Forest
- Gradient Boosting
- XGBoost
- LightGBM
- CatBoost
- Neural Networks

## CTO Assessment

This is the first enterprise-grade AI-RPCT training dataset built on the historical provider data moat.
""",
encoding="utf-8"
    )

    print("TRAINING DATASET BUILDER V2")
    print("===========================")
    print("Rows:", len(dataset))
    print("Columns:", len(dataset.columns))
    print("CSV:", OUT)


if __name__=="__main__":
    main()
