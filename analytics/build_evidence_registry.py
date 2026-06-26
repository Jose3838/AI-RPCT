from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

OUTPUTS = [
    DATA / "evidence_registry.csv",
    ROOT / "warehouse" / "metadata" / "evidence_registry.csv",
]

FIELDS = [
    "evidence_id",
    "decision_id",
    "evidence_type",
    "source_asset",
    "description",
]

ROWS = [
    {
        "evidence_id": "EV-0001",
        "decision_id": "decision-001",
        "evidence_type": "forecast",
        "source_asset": "forecast_engine_v1_output",
        "description": "Forecast confidence supports recommendation.",
    },
    {
        "evidence_id": "EV-0002",
        "decision_id": "decision-001",
        "evidence_type": "history",
        "source_asset": "decision_history",
        "description": "Historical decision archive available.",
    },
]


def main() -> None:
    for output in OUTPUTS:
        output.parent.mkdir(parents=True, exist_ok=True)

        with output.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(ROWS)

    print(f"Wrote {len(ROWS)} evidence records.")
    print(DATA / "evidence_registry.csv")


if __name__ == "__main__":
    main()
