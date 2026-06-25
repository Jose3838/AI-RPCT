from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

OUT = Path("warehouse/historical/provider_registry/aws_historical_provider_registry_v1.csv")
REPORT = Path("reports/aws_historical_provider_registry_v1.md")

ROWS = [
    {
        "provider": "AWS",
        "provider_family": "hyperscaler_family",
        "date": "2016-09-01",
        "event_type": "gpu_instance_family_available",
        "instance_family": "P2",
        "gpu_family": "K80_family",
        "representative_gpu": "NVIDIA K80",
        "region_scope": "multi_region",
        "data_type": "provider_gpu_catalog",
        "verification_status": "needs_source_link",
        "trust_grade": "B",
    },
    {
        "provider": "AWS",
        "provider_family": "hyperscaler_family",
        "date": "2017-10-01",
        "event_type": "gpu_instance_family_available",
        "instance_family": "P3",
        "gpu_family": "V100_family",
        "representative_gpu": "NVIDIA V100",
        "region_scope": "multi_region",
        "data_type": "provider_gpu_catalog",
        "verification_status": "needs_source_link",
        "trust_grade": "B",
    },
    {
        "provider": "AWS",
        "provider_family": "hyperscaler_family",
        "date": "2020-11-01",
        "event_type": "gpu_instance_family_available",
        "instance_family": "P4d",
        "gpu_family": "A100_family",
        "representative_gpu": "NVIDIA A100",
        "region_scope": "multi_region",
        "data_type": "provider_gpu_catalog",
        "verification_status": "needs_source_link",
        "trust_grade": "B",
    },
    {
        "provider": "AWS",
        "provider_family": "hyperscaler_family",
        "date": "2023-07-01",
        "event_type": "gpu_instance_family_available",
        "instance_family": "P5",
        "gpu_family": "H100_family",
        "representative_gpu": "NVIDIA H100",
        "region_scope": "multi_region",
        "data_type": "provider_gpu_catalog",
        "verification_status": "needs_source_link",
        "trust_grade": "B",
    },
]


def main() -> None:
    df = pd.DataFrame(ROWS)
    df["registry_version"] = "v1"
    df["created_at"] = datetime.now(UTC).isoformat()

    OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(OUT, index=False)

    REPORT.write_text(
        "\n".join([
            "# AWS Historical Provider Registry v1",
            "",
            f"Rows: {len(df)}",
            "",
            "## CTO Assessment",
            "",
            "This registry captures AWS GPU instance-family history in a normalized provider timeline format.",
            "Rows are structured historical catalog entries and should be upgraded with source URLs before commercial claims.",
            "",
        ]),
        encoding="utf-8",
    )

    print("AWS HISTORICAL PROVIDER REGISTRY V1")
    print("===================================")
    print(df)


if __name__ == "__main__":
    main()
