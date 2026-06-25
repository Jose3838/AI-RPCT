from __future__ import annotations

from pathlib import Path

import pandas as pd

TIMELINE = Path("warehouse/historical/master_timeline_v1.csv")
GPU = Path("warehouse/historical/gpu_history_registry_v1.csv")
EVENTS = Path("warehouse/historical/historical_market_events_registry_v1.csv")
PROVIDERS = Path("warehouse/historical/provider_registry/unified_provider_registry_v1.csv")

OUT = Path("warehouse/historical/enriched_historical_timeline_v1.csv")
REPORT = Path("reports/historical_timeline_enricher_v1.md")


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size <= 1:
        return pd.DataFrame()
    return pd.read_csv(path)


def month_start(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series, errors="coerce").dt.to_period("M").dt.to_timestamp().dt.strftime("%Y-%m-01")


def main() -> None:
    timeline = read_csv(TIMELINE)
    gpu = read_csv(GPU)
    events = read_csv(EVENTS)
    providers = read_csv(PROVIDERS)

    if timeline.empty:
        raise SystemExit("master_timeline_v1.csv missing or empty")

    timeline = timeline.copy()
    timeline["date"] = month_start(timeline["date"])

    gpu_count = pd.DataFrame()
    event_count = pd.DataFrame()
    provider_count = pd.DataFrame()

    if not gpu.empty:
        gpu["date"] = month_start(gpu["release_date"])
        gpu_count = (
            gpu.groupby("date")
            .agg(
                gpu_release_count=("representative_gpu", "count"),
                gpu_vendor_count=("vendor", "nunique"),
            )
            .reset_index()
        )

    if not events.empty:
        events["date"] = month_start(events["event_date"])
        event_count = (
            events.groupby("date")
            .agg(
                historical_event_count=("title", "count"),
                critical_event_count=("impact_level", lambda s: int((s == "critical").sum())),
            )
            .reset_index()
        )

    if not providers.empty:
        providers["date"] = month_start(providers["date"])
        provider_count = (
            providers.groupby("date")
            .agg(
                provider_catalog_event_count=("provider", "count"),
                provider_count=("provider", "nunique"),
                provider_gpu_family_count=("gpu_family", "nunique"),
            )
            .reset_index()
        )

    enriched = timeline.copy()

    for frame in [gpu_count, event_count, provider_count]:
        if not frame.empty:
            enriched = enriched.merge(frame, on="date", how="left")

    for col in [
        "gpu_release_count",
        "gpu_vendor_count",
        "historical_event_count",
        "critical_event_count",
        "provider_catalog_event_count",
        "provider_count",
        "provider_gpu_family_count",
    ]:
        if col not in enriched.columns:
            enriched[col] = 0
        enriched[col] = pd.to_numeric(enriched[col], errors="coerce").fillna(0).astype(int)

    enriched["historical_activity_score"] = (
        enriched["gpu_release_count"] * 3
        + enriched["critical_event_count"] * 3
        + enriched["historical_event_count"] * 2
        + enriched["provider_catalog_event_count"] * 2
        + enriched["provider_count"]
        + enriched["provider_gpu_family_count"]
    )

    enriched["timeline_enrichment_version"] = "v1"

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    enriched.to_csv(OUT, index=False)

    REPORT.write_text(
        "\n".join([
            "# Historical Timeline Enricher v1",
            "",
            f"Timeline rows: {len(enriched)}",
            f"GPU release months: {int((enriched['gpu_release_count'] > 0).sum())}",
            f"Historical event months: {int((enriched['historical_event_count'] > 0).sum())}",
            f"Provider catalog months: {int((enriched['provider_catalog_event_count'] > 0).sum())}",
            "",
            "## CTO Assessment",
            "",
            "This enriched timeline connects GPU history, market events, and provider catalog history to the canonical monthly timeline.",
            "It becomes the foundation for historical feature engineering and future time-series forecasting.",
            "",
        ]),
        encoding="utf-8",
    )

    print("HISTORICAL TIMELINE ENRICHER V1")
    print("===============================")
    print(enriched[[
        "date",
        "gpu_release_count",
        "historical_event_count",
        "provider_catalog_event_count",
        "historical_activity_score",
    ]].head(20))
    print(f"Rows: {len(enriched)}")
    print(f"CSV: {OUT}")


if __name__ == "__main__":
    main()
