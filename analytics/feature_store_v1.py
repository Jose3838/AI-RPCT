from __future__ import annotations

from pathlib import Path

import pandas as pd

FORECAST_FEATURES = Path("data/forecast_features_v1.csv")
MARKET_REGIME = Path("data/market_regime_v1.csv")
HISTORICAL = Path("data/historical_master_dataset.csv")
OUT = Path("data/feature_store_v1.csv")
REPORT = Path("reports/feature_store_v1.md")


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size <= 1:
        return pd.DataFrame()
    return pd.read_csv(path)


def main() -> None:
    features = read_csv(FORECAST_FEATURES)
    regimes = read_csv(MARKET_REGIME)
    historical = read_csv(HISTORICAL)

    if features.empty:
        raise SystemExit("forecast_features_v1.csv missing or empty")

    store = features.copy()

    if not regimes.empty:
        store = store.merge(
            regimes[["provider", "gpu", "market_regime", "confidence"]],
            on=["provider", "gpu"],
            how="left",
            suffixes=("", "_regime"),
        )

    gpu_release_count = 0
    market_event_count = 0

    if not historical.empty and "dataset" in historical.columns:
        gpu_release_count = int((historical["dataset"] == "gpu_releases").sum())
        market_event_count = int((historical["dataset"] == "market_events").sum())

    store["historical_gpu_release_count"] = gpu_release_count
    store["historical_market_event_count"] = market_event_count
    store["feature_store_version"] = "v1"

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    store.to_csv(OUT, index=False)

    REPORT.write_text(
        "\n".join(
            [
                "# Feature Store v1",
                "",
                f"Feature rows: {len(store)}",
                f"Historical GPU releases: {gpu_release_count}",
                f"Historical market events: {market_event_count}",
                "",
                "## CTO Assessment",
                "",
                "Feature Store v1 centralizes forecast-ready provider/GPU features.",
                "Future forecast engines should use this store instead of rebuilding features independently.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print("FEATURE STORE V1")
    print("================")
    print(f"Rows: {len(store)}")
    print(f"CSV: {OUT}")
    print(f"Report: {REPORT}")


if __name__ == "__main__":
    main()
