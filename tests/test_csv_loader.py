import csv
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analytics"))

from builders.csv_loader import load_csv, index_by, group_by, unique_values


def write_sample_csv(path):
    path.parent.mkdir(parents=True, exist_ok=True)

    rows = [
        {"id": "a", "type": "gpu", "name": "Alpha"},
        {"id": "b", "type": "gpu", "name": "Beta"},
        {"id": "c", "type": "cpu", "name": "Gamma"},
    ]

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "type", "name"])
        writer.writeheader()
        writer.writerows(rows)


def test_load_csv(tmp_path):
    path = tmp_path / "sample.csv"
    write_sample_csv(path)

    rows = load_csv(path)

    assert len(rows) == 3
    assert rows[0]["id"] == "a"


def test_index_by(tmp_path):
    path = tmp_path / "sample.csv"
    write_sample_csv(path)

    rows = load_csv(path)
    indexed = index_by(rows, "id")

    assert indexed["b"]["name"] == "Beta"


def test_group_by(tmp_path):
    path = tmp_path / "sample.csv"
    write_sample_csv(path)

    rows = load_csv(path)
    grouped = group_by(rows, "type")

    assert len(grouped["gpu"]) == 2
    assert len(grouped["cpu"]) == 1


def test_unique_values(tmp_path):
    path = tmp_path / "sample.csv"
    write_sample_csv(path)

    rows = load_csv(path)

    assert unique_values(rows, "type") == {"gpu", "cpu"}
