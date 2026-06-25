from __future__ import annotations

from pathlib import Path

import pandas as pd

FEATURE_STORE = Path("data/feature_store_v1.csv")
FORECAST = Path("data/forecast_engine_v4.csv")
OUTCOME = Path("data/forecast_outcome_tracker_v1.csv")

OUT = Path("data/training_dataset_v1.csv")
REPORT = Path("reports/training_dataset_builder_v1.md")


def read(path: Path):
    if not path.exists() or path.stat().st_size <= 1:
        return pd.DataFrame()
    return pd.read_csv(path)


def main():

    features = read(FEATURE_STORE)
    forecasts = read(FORECAST)
    outcomes = read(OUTCOME)

    if features.empty:
        raise SystemExit("Feature Store missing")

    dataset = features.merge(
        forecasts[
            [
                "provider",
                "gpu",
                "forecast_score",
                "forecast_signal",
            ]
        ],
        on=["provider", "gpu"],
        how="left",
    )

    if not outcomes.empty:

        latest = (
            outcomes
            .sort_values("snapshot_timestamp")
            .groupby(["provider", "gpu"])
            .tail(1)
        )

        latest = latest.rename(
            columns={
                "current_market_regime":"future_market_regime"
            }
        )

        dataset = dataset.merge(
            latest[
                [
                    "provider",
                    "gpu",
                    "future_market_regime"
                ]
            ],
            on=["provider","gpu"],
            how="left"
        )

    dataset["training_version"]="v1"

    OUT.parent.mkdir(exist_ok=True)
    REPORT.parent.mkdir(exist_ok=True)

    dataset.to_csv(OUT,index=False)

    REPORT.write_text(
f"""# Training Dataset Builder v1

Rows: {len(dataset)}

Columns: {len(dataset.columns)}

Purpose:

This dataset combines

- feature store
- forecast engine
- future outcomes

to prepare AI-RPCT for learning models.
""",
encoding="utf-8"
)

    print("TRAINING DATASET BUILDER")
    print("========================")
    print(f"Rows: {len(dataset)}")
    print(f"Columns: {len(dataset.columns)}")
    print(f"CSV: {OUT}")

if __name__=="__main__":
    main()
