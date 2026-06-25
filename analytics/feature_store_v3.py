from __future__ import annotations

from pathlib import Path

import pandas as pd

FEATURES = Path("data/feature_store_v2.csv")
TIMELINE = Path("warehouse/historical/enriched_historical_timeline_v1.csv")

OUT = Path("data/feature_store_v3.csv")
REPORT = Path("reports/feature_store_v3.md")


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size <= 1:
        return pd.DataFrame()
    return pd.read_csv(path)


def month_start(series: pd.Series) -> pd.Series:
    return (
        pd.to_datetime(series, errors="coerce")
        .dt.to_period("M")
        .dt.to_timestamp()
        .dt.strftime("%Y-%m-01")
    )


def main() -> None:
    features = read_csv(FEATURES)
    timeline = read_csv(TIMELINE)

    if features.empty:
        raise SystemExit("feature_store_v2.csv missing or empty")

    store = features.copy()

    if "latest_timestamp" in store.columns:
        store["timeline_month"] = month_start(store["latest_timestamp"])
    else:
        store["timeline_month"] = ""

    if not timeline.empty:
        timeline = timeline.copy()
        timeline["timeline_month"] = month_start(timeline["date"])

        timeline_cols = [
            "timeline_month",
            "gpu_release_count",
            "historical_event_count",
            "critical_event_count",
            "provider_catalog_event_count",
            "provider_count",
            "provider_gpu_family_count",
            "historical_activity_score",
        ]

        available_cols = [col for col in timeline_cols if col in timeline.columns]

        store = store.merge(
            timeline[available_cols],
            on="timeline_month",
            how="left",
        )

    for col in [
        "gpu_release_count",
        "historical_event_count",
        "critical_event_count",
        "provider_catalog_event_count",
        "provider_count",
        "provider_gpu_family_count",
        "historical_activity_score",
    ]:
        if col not in store.columns:
            store[col] = 0
        store[col] = pd.to_numeric(store[col], errors="coerce").fillna(0).astype(int)

    store["feature_store_version"] = "v3"
    store["historical_timeline_enrichment"] = "v1"

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    store.to_csv(OUT, index=False)

    REPORT.write_text(
        "\n".join([
            "# Feature Store v3",
            "",
            f"Rows: {len(store)}",
            f"Columns: {len(store.columns)}",
            "",
            "## Added Historical Timeline Features",
            "",
            "- gpu_release_count",
            "- historical_event_count",
            "- critical_event_count",
            "- provider_catalog_event_count",
            "- provider_count",
            "- provider_gpu_family_count",
            "- historical_activity_score",
            "",
            "## CTO Assessment",
            "",
            "Feature Store v3 enriches live provider/GPU features with the canonical historical timeline.",
            "This connects current market observations to historical infrastructure context.",
            "",
        ]),
        encoding="utf-8",
    )

    print("FEATURE STORE V3")
    print("================")
    print(f"Rows: {len(store)}")
    print(f"Columns: {len(store.columns)}")
    print(f"CSV: {OUT}")


if __name__ == "__main__":
    main()
