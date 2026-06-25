import csv
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analytics"))

from builders.csv_writer import write_registry_csv


def test_write_registry_csv_writes_data_and_warehouse(tmp_path):
    columns = ["id", "name"]
    rows = [{"id": "1", "name": "Alpha"}]

    data_path = tmp_path / "data" / "sample.csv"
    warehouse_path = tmp_path / "warehouse" / "sample.csv"

    write_registry_csv(
        columns=columns,
        rows=rows,
        data_path=data_path,
        warehouse_path=warehouse_path,
    )

    assert data_path.exists()
    assert warehouse_path.exists()

    with data_path.open(newline="", encoding="utf-8") as f:
        data_rows = list(csv.DictReader(f))

    with warehouse_path.open(newline="", encoding="utf-8") as f:
        warehouse_rows = list(csv.DictReader(f))

    assert data_rows == rows
    assert warehouse_rows == rows
