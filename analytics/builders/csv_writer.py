from __future__ import annotations

import csv
from pathlib import Path


def write_registry_csv(
    *,
    columns: list[str],
    rows: list[dict[str, str]],
    data_path: Path,
    warehouse_path: Path,
) -> None:
    for path in [data_path, warehouse_path]:
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()
            writer.writerows(rows)


def print_registry_result(
    *,
    row_count: int,
    label: str,
    data_path: Path,
    warehouse_path: Path,
) -> None:
    print(f"Wrote {row_count} {label}.")
    print(data_path)
    print(warehouse_path)
