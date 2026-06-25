import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analytics"))

from builders import registry_builder


def test_write_registry_creates_data_and_warehouse_files(tmp_path, monkeypatch):
    monkeypatch.setattr(registry_builder, "ROOT", tmp_path)

    rows = [{"id": "1", "name": "Alpha"}]
    columns = ["id", "name"]

    registry_builder.write_registry(
        rows=rows,
        columns=columns,
        registry_name="sample_registry",
        warehouse_group="metadata",
        label="sample records",
    )

    data_path = tmp_path / "data" / "sample_registry.csv"

    warehouse_path = (
        tmp_path
        / "warehouse"
        / "metadata"
        / "sample_registry.csv"
    )

    assert data_path.exists()
    assert warehouse_path.exists()

    with data_path.open(newline="", encoding="utf-8") as f:
        data_rows = list(csv.DictReader(f))

    assert data_rows == rows
