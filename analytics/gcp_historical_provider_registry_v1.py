from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

OUT = Path("warehouse/historical/provider_registry/gcp_historical_provider_registry_v1.csv")
REPORT = Path("reports/gcp_historical_provider_registry_v1.md")

ROWS = [
    {
        "provider": "Google Cloud",
        "provider_family": "hyperscaler_family",
        "date": "2017-02-01",
        "event_type": "gpu_accelerator_available",
        "instance_family": "K80 accelerator",
        "gpu_family": "K80_family",
        "representative_gpu": "NVIDIA K80",
        "region_scope": "multi_region",
        "data_type": "provider_gpu_catalog",
        "verification_status": "needs_source_link",
        "trust_grade": "B",
    },
    {
        "provider": "Google Cloud",
        "provider_family": "hyperscaler_family",
        "date": "2018-02-01",
        "event_type": "gpu_accelerator_available",
        "instance_family": "V100 accelerator",
        "gpu_family": "V100_family",
        "representative_gpu": "NVIDIA V100",
        "region_scope": "multi_region",
        "data_type": "provider_gpu_catalog",
        "verification_status": "needs_source_link",
        "trust_grade": "B",
    },
    {
        "provider": "Google Cloud",
        "provider_family": "hyperscaler_family",
        "date": "2021-05-01",
        "event_type": "gpu_accelerator_available",
        "instance_family": "A2",
        "gpu_family": "A100_family",
        "representative_gpu": "NVIDIA A100",
        "region_scope": "multi_region",
        "data_type": "provider_gpu_catalog",
        "verification_status": "needs_source_link",
        "trust_grade": "B",
    },
    {
        "provider": "Google Cloud",
        "provider_family": "hyperscaler_family",
        "date": "2023-09-01",
        "event_type": "gpu_accelerator_available",
        "instance_family": "A3",
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
            "# Google Cloud Historical Provider Registry v1",
            "",
            f"Rows: {len(df)}",
            "",
            "## CTO Assessment",
            "",
            "This registry captures Google Cloud GPU accelerator history in a normalized provider timeline format.",
            "Rows are structured historical catalog entries and should be upgraded with source URLs before commercial claims.",
            "",
        ]),
        encoding="utf-8",
    )

    print("GCP HISTORICAL PROVIDER REGISTRY V1")
    print("===================================")
    print(df)


if __name__ == "__main__":
    main()
