from __future__ import annotations

import csv
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

from collectors.providers.vast_real import VastRealProvider
from collectors.providers.runpod_real import RunPodRealProvider

DATA_DIR = Path("data")
WAREHOUSE_DIR = Path("warehouse/live_provider_history")

STATUS_PATH = DATA_DIR / "live_provider_ingestion_status.csv"

STATUS_FIELDS = [
    "provider",
    "status",
    "fresh_rows",
    "used_fallback",
    "output_file",
    "error",
    "timestamp",
]


def normalize_provider_name(name: str) -> str:
    return name.replace("_real", "")


def write_status(rows: list[dict]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with STATUS_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=STATUS_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def run_provider(provider) -> dict:
    provider_name = normalize_provider_name(provider.name)
    timestamp = datetime.now(UTC).isoformat()

    try:
        rows = provider.fetch()
        fresh_rows = len(rows)

        output_file = DATA_DIR / f"{provider_name}_live_report.csv"

        if fresh_rows > 0:
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            WAREHOUSE_DIR.mkdir(parents=True, exist_ok=True)

            df = pd.DataFrame(rows)
            df.to_csv(output_file, index=False)

            date_key = datetime.now(UTC).date().isoformat()
            warehouse_file = WAREHOUSE_DIR / f"{date_key}_{provider_name}.csv"
            df.to_csv(warehouse_file, index=False)

            return {
                "provider": provider_name,
                "status": "fresh",
                "fresh_rows": fresh_rows,
                "used_fallback": False,
                "output_file": str(output_file),
                "error": "",
                "timestamp": timestamp,
            }

        return {
            "provider": provider_name,
            "status": "empty",
            "fresh_rows": 0,
            "used_fallback": True,
            "output_file": str(output_file),
            "error": "provider returned zero rows",
            "timestamp": timestamp,
        }

    except Exception as exc:
        return {
            "provider": provider_name,
            "status": "error",
            "fresh_rows": 0,
            "used_fallback": True,
            "output_file": f"data/{provider_name}_live_report.csv",
            "error": str(exc),
            "timestamp": timestamp,
        }


def main() -> None:
    providers = [
        VastRealProvider(),
        RunPodRealProvider(),
    ]

    rows = [run_provider(provider) for provider in providers]
    write_status(rows)

    print("LIVE PROVIDER INGESTION")
    print("=======================")
    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
