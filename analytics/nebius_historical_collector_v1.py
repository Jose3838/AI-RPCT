from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

OUT = Path("warehouse/historical/provider_capacity/nebius_historical_gpu_capacity_v1.csv")
REPORT = Path("reports/nebius_historical_collector_v1.md")

ROWS = [
    {"date": "2024-01-01", "provider": "Nebius", "provider_family": "specialized_gpu_cloud_family", "gpu_family": "H100_family", "gpu": "H100", "capacity_signal": "european_ai_cloud_capacity", "region": "eu", "source_basis": "historical_structure_placeholder"},
    {"date": "2024-06-01", "provider": "Nebius", "provider_family": "specialized_gpu_cloud_family", "gpu_family": "H200_family", "gpu": "H200", "capacity_signal": "next_generation_ai_cloud_capacity", "region": "eu", "source_basis": "historical_structure_placeholder"},
    {"date": "2025-01-01", "provider": "Nebius", "provider_family": "specialized_gpu_cloud_family", "gpu_family": "B200_family", "gpu": "B200", "capacity_signal": "blackwell_capacity_planned", "region": "eu", "source_basis": "historical_structure_placeholder"},
]


def main() -> None:
    df = pd.DataFrame(ROWS)
    df["source"] = "Nebius historical collector"
    df["trust_grade"] = "C"
    df["collector_version"] = "v1"
    df["created_at"] = datetime.now(UTC).isoformat()

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(OUT, index=False)

    REPORT.write_text(
        "\n".join([
            "# Nebius Historical Collector v1",
            "",
            f"Rows: {len(df)}",
            "",
            "## CTO Assessment",
            "",
            "This collector establishes Nebius European GPU cloud capacity structure.",
            "Rows are structural placeholders and must be upgraded with verified source-backed capacity evidence.",
            "",
        ]),
        encoding="utf-8",
    )

    print("NEBIUS HISTORICAL COLLECTOR V1")
    print("==============================")
    print(f"Rows: {len(df)}")
    print(f"CSV: {OUT}")


if __name__ == "__main__":
    main()
