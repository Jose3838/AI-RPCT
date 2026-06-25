from __future__ import annotations

from pathlib import Path

import pandas as pd

INPUT = Path("data/combined_market_intelligence_dataset.csv")
OUTPUT = Path("data/forecast_features_v1.csv")
REPORT = Path("reports/forecast_features_v1.md")


def read_input() -> pd.DataFrame:
    if not INPUT.exists() or INPUT.stat().st_size <= 1:
        return pd.DataFrame()
    return pd.read_csv(INPUT)


def build_live_provider_features(df: pd.DataFrame) -> pd.DataFrame:
    live = df[df.get("intelligence_layer") == "live_provider_timeseries"].copy()

    if live.empty:
        return pd.DataFrame()

    live["price_per_hour"] = pd.to_numeric(live.get("price_per_hour"), errors="coerce").fillna(0)
    live["availability"] = pd.to_numeric(live.get("availability"), errors="coerce").fillna(0)

    group_cols = ["provider", "gpu"]

    features = (
        live.groupby(group_cols, dropna=False)
        .agg(
            record_count=("provider", "count"),
            avg_price=("price_per_hour", "mean"),
            min_price=("price_per_hour", "min"),
            max_price=("price_per_hour", "max"),
            availability_sum=("availability", "sum"),
            latest_timestamp=("timestamp", "max"),
        )
        .reset_index()
    )

    features["avg_price"] = features["avg_price"].round(4)
    features["price_spread"] = (features["max_price"] - features["min_price"]).round(4)
    features["feature_layer"] = "live_provider_forecast_features"

    return features


def main() -> None:
    df = read_input()
    features = build_live_provider_features(df)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    features.to_csv(OUTPUT, index=False)

    provider_count = features["provider"].nunique() if not features.empty else 0
    gpu_count = features["gpu"].nunique() if not features.empty else 0

    REPORT.write_text(
        "\n".join(
            [
                "# Forecast Feature Builder v1",
                "",
                f"Input rows: {len(df)}",
                f"Feature rows: {len(features)}",
                f"Providers: {provider_count}",
                f"GPUs: {gpu_count}",
                "",
                "## CTO Assessment",
                "",
                "This feature set aggregates live provider time-series data into provider/GPU level signals.",
                "It is the first bridge from raw intelligence data toward forecast-ready features.",
                "",
                "## Next Step",
                "",
                "Build Forecast Engine v1 using avg_price, price_spread, record_count, and availability_sum.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print("FORECAST FEATURE BUILDER V1")
    print("===========================")
    print(f"Input rows   : {len(df)}")
    print(f"Feature rows : {len(features)}")
    print(f"CSV          : {OUTPUT}")
    print(f"Report       : {REPORT}")


if __name__ == "__main__":
    main()
