from __future__ import annotations

from pathlib import Path

from builders.csv_writer import (
    print_registry_result,
    write_registry_csv,
)

ROOT = Path(__file__).resolve().parents[2]


def write_registry(
    *,
    rows: list[dict[str, str]],
    columns: list[str],
    data_filename: str,
    warehouse_parts: list[str],
    label: str,
) -> None:
    data_path = ROOT / "data" / data_filename

    warehouse_path = ROOT / "warehouse"
    for part in warehouse_parts:
        warehouse_path = warehouse_path / part

    write_registry_csv(
        columns=columns,
        rows=rows,
        data_path=data_path,
        warehouse_path=warehouse_path,
    )

    print_registry_result(
        row_count=len(rows),
        label=label,
        data_path=data_path,
        warehouse_path=warehouse_path,
    )
