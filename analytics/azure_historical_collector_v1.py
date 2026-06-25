from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

OUT = Path("warehouse/historical/provider_pricing/azure_historical_gpu_pricing_v1.csv")
REPORT = Path("reports/azure_historical_collector_v1.md")

ROWS = [
    {"date": "2017-01-01", "provider": "Azure", "provider_family": "hyperscaler_family", "gpu_family": "K80_family", "gpu": "K80", "instance": "NC", "price_per_hour": 0, "region": "global", "price_basis": "placeholder"},
    {"date": "2018-01-01", "provider": "Azure", "provider_family": "hyperscaler_family", "gpu_family": "V100_family", "gpu": "V100", "instance": "NCv3", "price_per_hour": 0, "region": "global", "price_basis": "placeholder"},
    {"date": "2020-01-01", "provider": "Azure", "provider_family": "hyperscaler_family", "gpu_family": "A100_family", "gpu": "A100", "instance": "ND A100 v4", "price_per_hour": 0, "region": "global", "price_basis": "placeholder"},
    {"date": "2023-01-01", "provider": "Azure", "provider_family": "hyperscaler_family", "gpu_family": "H100_family", "gpu": "H100", "instance": "ND H100 v5", "price_per_hour": 0, "region": "global", "price_basis": "placeholder"},
]


def main() -> None:
    df = pd.DataFrame(ROWS)
    df["source"] = "Azure historical collector"
    df["trust_grade"] = "B"
    df["collector_version"] = "v1"
    df["created_at"] = datetime.now(UTC).isoformat()

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(OUT, index=False)

    REPORT.write_text(
        "\n".join([
            "# Azure Historical Collector v1",
            "",
            f"Rows: {len(df)}",
            "",
            "## CTO Assessment",
            "",
            "This collector establishes the Azure historical GPU VM structure.",
            "Prices are placeholders and must be replaced with verified historical pricing before commercial price-forecast claims.",
            "",
        ]),
        encoding="utf-8",
    )

    print("AZURE HISTORICAL COLLECTOR V1")
    print("=============================")
    print(f"Rows: {len(df)}")
    print(f"CSV: {OUT}")


if __name__ == "__main__":
    main()
