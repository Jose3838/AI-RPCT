from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

OUT = Path("warehouse/historical/provider_capacity/coreweave_historical_gpu_capacity_v1.csv")
REPORT = Path("reports/coreweave_historical_collector_v1.md")

ROWS = [
    {"date": "2019-01-01", "provider": "CoreWeave", "provider_family": "specialized_gpu_cloud_family", "gpu_family": "V100_family", "gpu": "V100", "capacity_signal": "early_gpu_cloud", "region": "us", "source_basis": "historical_structure_placeholder"},
    {"date": "2021-01-01", "provider": "CoreWeave", "provider_family": "specialized_gpu_cloud_family", "gpu_family": "A100_family", "gpu": "A100", "capacity_signal": "ai_training_capacity", "region": "us", "source_basis": "historical_structure_placeholder"},
    {"date": "2023-01-01", "provider": "CoreWeave", "provider_family": "specialized_gpu_cloud_family", "gpu_family": "H100_family", "gpu": "H100", "capacity_signal": "high_demand_training_capacity", "region": "us", "source_basis": "historical_structure_placeholder"},
    {"date": "2024-01-01", "provider": "CoreWeave", "provider_family": "specialized_gpu_cloud_family", "gpu_family": "H200_family", "gpu": "H200", "capacity_signal": "next_generation_capacity", "region": "us", "source_basis": "historical_structure_placeholder"},
]


def main() -> None:
    df = pd.DataFrame(ROWS)
    df["source"] = "CoreWeave historical collector"
    df["trust_grade"] = "C"
    df["collector_version"] = "v1"
    df["created_at"] = datetime.now(UTC).isoformat()

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(OUT, index=False)

    REPORT.write_text(
        "\n".join([
            "# CoreWeave Historical Collector v1",
            "",
            f"Rows: {len(df)}",
            "",
            "## CTO Assessment",
            "",
            "This collector establishes specialized GPU cloud capacity structure for CoreWeave.",
            "Rows are structural placeholders and must be upgraded with verified source-backed capacity/pricing evidence.",
            "",
        ]),
        encoding="utf-8",
    )

    print("COREWEAVE HISTORICAL COLLECTOR V1")
    print("=================================")
    print(f"Rows: {len(df)}")
    print(f"CSV: {OUT}")


if __name__ == "__main__":
    main()
