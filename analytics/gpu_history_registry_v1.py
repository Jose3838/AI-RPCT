from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

OUT = Path("warehouse/historical/gpu_history_registry_v1.csv")
REPORT = Path("reports/gpu_history_registry_v1.md")

ROWS = [
    {
        "release_date": "2006-11-01",
        "vendor": "NVIDIA",
        "architecture": "Tesla",
        "gpu_generation": "Tesla_family",
        "representative_gpu": "GeForce 8800 GTX",
        "market_role": "consumer_foundation",
        "source_status": "verified_release_date",
        "trust_grade": "A",
    },
    {
        "release_date": "2008-06-01",
        "vendor": "NVIDIA",
        "architecture": "Tesla Compute",
        "gpu_generation": "Tesla_compute_family",
        "representative_gpu": "Tesla C1060",
        "market_role": "gpu_compute",
        "source_status": "verified_release_date",
        "trust_grade": "A",
    },
    {
        "release_date": "2012-03-01",
        "vendor": "NVIDIA",
        "architecture": "Kepler",
        "gpu_generation": "Kepler_family",
        "representative_gpu": "Tesla K20",
        "market_role": "datacenter",
        "source_status": "verified_release_date",
        "trust_grade": "A",
    },
    {
        "release_date": "2014-11-01",
        "vendor": "NVIDIA",
        "architecture": "Maxwell",
        "gpu_generation": "Maxwell_family",
        "representative_gpu": "Tesla M40",
        "market_role": "datacenter",
        "source_status": "verified_release_date",
        "trust_grade": "A",
    },
    {
        "release_date": "2016-04-01",
        "vendor": "NVIDIA",
        "architecture": "Pascal",
        "gpu_generation": "Pascal_family",
        "representative_gpu": "Tesla P100",
        "market_role": "datacenter",
        "source_status": "verified_release_date",
        "trust_grade": "A",
    },
    {
        "release_date": "2017-05-01",
        "vendor": "NVIDIA",
        "architecture": "Volta",
        "gpu_generation": "Volta_family",
        "representative_gpu": "Tesla V100",
        "market_role": "ai_training",
        "source_status": "verified_release_date",
        "trust_grade": "A",
    },
    {
        "release_date": "2020-05-01",
        "vendor": "NVIDIA",
        "architecture": "Ampere",
        "gpu_generation": "Ampere_family",
        "representative_gpu": "A100",
        "market_role": "ai_training",
        "source_status": "verified_release_date",
        "trust_grade": "A",
    },
    {
        "release_date": "2022-03-01",
        "vendor": "NVIDIA",
        "architecture": "Hopper",
        "gpu_generation": "Hopper_family",
        "representative_gpu": "H100",
        "market_role": "foundation_models",
        "source_status": "verified_release_date",
        "trust_grade": "A",
    },
    {
        "release_date": "2024-03-01",
        "vendor": "NVIDIA",
        "architecture": "Blackwell",
        "gpu_generation": "Blackwell_family",
        "representative_gpu": "B200",
        "market_role": "next_generation_ai",
        "source_status": "verified_release_date",
        "trust_grade": "A",
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
            "# GPU History Registry v1",
            "",
            f"Rows: {len(df)}",
            "",
            "## CTO Assessment",
            "",
            "This registry provides a structured chronology of major NVIDIA GPU architectures.",
            "It serves as a reference layer for future historical provider, pricing, and market-event datasets.",
        ]),
        encoding="utf-8",
    )

    print("GPU HISTORY REGISTRY V1")
    print("=======================")
    print(df)


if __name__ == "__main__":
    main()
