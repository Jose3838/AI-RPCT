from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

OUT = Path("warehouse/historical/provider_pricing/lambda_historical_gpu_pricing_v1.csv")
REPORT = Path("reports/lambda_historical_collector_v1.md")

ROWS = [
    {"date": "2018-01-01", "provider": "Lambda", "provider_family": "specialized_gpu_cloud_family", "gpu_family": "V100_family", "gpu": "V100", "instance": "gpu_cloud", "price_per_hour": 0, "region": "us", "price_basis": "placeholder"},
    {"date": "2021-01-01", "provider": "Lambda", "provider_family": "specialized_gpu_cloud_family", "gpu_family": "A100_family", "gpu": "A100", "instance": "gpu_cloud", "price_per_hour": 0, "region": "us", "price_basis": "placeholder"},
    {"date": "2023-01-01", "provider": "Lambda", "provider_family": "specialized_gpu_cloud_family", "gpu_family": "H100_family", "gpu": "H100", "instance": "gpu_cloud", "price_per_hour": 0, "region": "us", "price_basis": "placeholder"},
    {"date": "2024-01-01", "provider": "Lambda", "provider_family": "specialized_gpu_cloud_family", "gpu_family": "H200_family", "gpu": "H200", "instance": "gpu_cloud", "price_per_hour": 0, "region": "us", "price_basis": "placeholder"},
]


def main() -> None:
    df = pd.DataFrame(ROWS)
    df["source"] = "Lambda historical collector"
    df["trust_grade"] = "C"
    df["collector_version"] = "v1"
    df["created_at"] = datetime.now(UTC).isoformat()

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(OUT, index=False)

    REPORT.write_text(
        "\n".join([
            "# Lambda Historical Collector v1",
            "",
            f"Rows: {len(df)}",
            "",
            "## CTO Assessment",
            "",
            "This collector establishes Lambda GPU cloud pricing structure.",
            "Prices are placeholders and must be replaced with verified source-backed pricing before commercial price-forecast claims.",
            "",
        ]),
        encoding="utf-8",
    )

    print("LAMBDA HISTORICAL COLLECTOR V1")
    print("==============================")
    print(f"Rows: {len(df)}")
    print(f"CSV: {OUT}")


if __name__ == "__main__":
    main()
