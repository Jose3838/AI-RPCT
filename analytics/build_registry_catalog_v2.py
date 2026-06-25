from __future__ import annotations

import csv
from pathlib import Path

from builders.csv_writer import (
    write_registry_csv,
    print_registry_result,
)

ROOT = Path(__file__).resolve().parents[1]

COLUMNS = [
    "registry_name",
    "relative_path",
    "row_count",
]


def count_rows(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as f:
        return max(sum(1 for _ in csv.reader(f)) - 1, 0)


def build_rows():
    rows = []

    for csv_file in sorted((ROOT / "data").glob("*.csv")):
        rows.append(
            {
                "registry_name": csv_file.stem,
                "relative_path": str(csv_file.relative_to(ROOT)),
                "row_count": str(count_rows(csv_file)),
            }
        )

    return rows


def main():
    rows = build_rows()

    data_path = ROOT / "data" / "registry_catalog_v2.csv"

    warehouse_path = (
        ROOT
        / "warehouse"
        / "metadata"
        / "registry_catalog_v2.csv"
    )

    write_registry_csv(
        columns=COLUMNS,
        rows=rows,
        data_path=data_path,
        warehouse_path=warehouse_path,
    )

    print_registry_result(
        row_count=len(rows),
        label="registry catalog records",
        data_path=data_path,
        warehouse_path=warehouse_path,
    )


if __name__ == "__main__":
    main()
