from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path("warehouse/historical")
OUT = Path("data/unified_historical_provider_dataset_v1.csv")
REPORT = Path("reports/unified_historical_collector_pipeline_v1.md")


def main() -> None:
    frames = []

    for path in ROOT.rglob("*_historical_*_v1.csv"):
        try:
            df = pd.read_csv(path)
            df["source_file"] = str(path)
            df["historical_dataset_type"] = path.parent.name
            frames.append(df)
        except Exception as error:
            print(f"Skipped {path}: {error}")

    if frames:
        combined = pd.concat(frames, ignore_index=True, sort=False)
    else:
        combined = pd.DataFrame()

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    combined.to_csv(OUT, index=False)

    providers = combined["provider"].nunique() if "provider" in combined.columns and not combined.empty else 0
    rows = len(combined)

    REPORT.write_text(
        "\n".join(
            [
                "# Unified Historical Collector Pipeline v1",
                "",
                f"Rows: {rows}",
                f"Providers: {providers}",
                "",
                "## CTO Assessment",
                "",
                "This pipeline unifies all historical provider collector outputs into one provider history dataset.",
                "It is the integration layer required before Feature Store v2.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print("UNIFIED HISTORICAL COLLECTOR PIPELINE V1")
    print("========================================")
    print(f"Rows: {rows}")
    print(f"Providers: {providers}")
    print(f"CSV: {OUT}")


if __name__ == "__main__":
    main()
