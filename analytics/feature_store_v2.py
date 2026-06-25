from __future__ import annotations

from pathlib import Path

import pandas as pd

FEATURES = Path("data/feature_store_family_provider_v1.csv")
HISTORICAL = Path("data/unified_historical_provider_dataset_v1.csv")

OUT = Path("data/feature_store_v2.csv")
REPORT = Path("reports/feature_store_v2.md")


def read(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size <= 1:
        return pd.DataFrame()
    return pd.read_csv(path)


def main() -> None:
    features = read(FEATURES)
    historical = read(HISTORICAL)

    if features.empty:
        raise SystemExit("feature_store_family_provider_v1.csv missing or empty")

    store = features.copy()

    historical_provider_count = 0
    historical_gpu_family_count = 0

    if not historical.empty:
        historical_provider_count = historical["provider"].nunique() if "provider" in historical.columns else 0
        historical_gpu_family_count = historical["gpu_family"].nunique() if "gpu_family" in historical.columns else 0

        coverage = (
            historical.groupby(["provider_family", "gpu_family"], dropna=False)
            .size()
            .reset_index(name="historical_family_rows")
        )

        store = store.merge(
            coverage,
            on=["provider_family", "gpu_family"],
            how="left",
        )
    else:
        store["historical_family_rows"] = 0

    store["historical_family_rows"] = (
        pd.to_numeric(store["historical_family_rows"], errors="coerce")
        .fillna(0)
        .astype(int)
    )

    store["historical_provider_count"] = historical_provider_count
    store["historical_gpu_family_count"] = historical_gpu_family_count
    store["feature_store_version"] = "v2"

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    store.to_csv(OUT, index=False)

    REPORT.write_text(
        "\n".join(
            [
                "# Feature Store v2",
                "",
                f"Feature rows: {len(store)}",
                f"Historical providers: {historical_provider_count}",
                f"Historical GPU families: {historical_gpu_family_count}",
                "",
                "## CTO Assessment",
                "",
                "Feature Store v2 enriches live forecast features with unified historical provider coverage.",
                "This is the first feature store version that directly incorporates the historical provider data moat.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print("FEATURE STORE V2")
    print("================")
    print(f"Rows: {len(store)}")
    print(f"Historical providers: {historical_provider_count}")
    print(f"Historical GPU families: {historical_gpu_family_count}")
    print(f"CSV: {OUT}")


if __name__ == "__main__":
    main()
