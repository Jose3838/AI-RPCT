from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path("warehouse/historical/provider_registry")
OUT = Path("warehouse/historical/provider_registry/unified_provider_registry_v1.csv")
REPORT = Path("reports/unified_provider_registry_v1.md")


def main() -> None:
    frames = []

    for path in ROOT.glob("*_historical_provider_registry_v1.csv"):
        df = pd.read_csv(path)
        df["source_file"] = path.name
        frames.append(df)

    if frames:
        unified = pd.concat(frames, ignore_index=True, sort=False)
        unified = unified.sort_values(["date", "provider", "gpu_family"])
    else:
        unified = pd.DataFrame()

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    unified.to_csv(OUT, index=False)

    providers = unified["provider"].nunique() if not unified.empty and "provider" in unified.columns else 0
    rows = len(unified)

    REPORT.write_text(
        "\n".join([
            "# Unified Provider Registry v1",
            "",
            f"Rows: {rows}",
            f"Providers: {providers}",
            "",
            "## CTO Assessment",
            "",
            "This registry consolidates normalized historical provider catalog entries.",
            "It is the provider-history counterpart to the master timeline and GPU history registry.",
            "",
            "Next step: join this registry against the master timeline to create timeline-aware provider features.",
            "",
        ]),
        encoding="utf-8",
    )

    print("UNIFIED PROVIDER REGISTRY V1")
    print("============================")
    print(f"Rows: {rows}")
    print(f"Providers: {providers}")
    print(f"CSV: {OUT}")


if __name__ == "__main__":
    main()
