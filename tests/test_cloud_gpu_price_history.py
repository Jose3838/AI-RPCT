import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CSV_PATH = ROOT / "data" / "cloud_gpu_price_history.csv"
WAREHOUSE_PATH = ROOT / "warehouse" / "historical" / "providers" / "cloud_gpu_price_history.csv"

REQUIRED_COLUMNS = {
    "observation_id",
    "provider_id",
    "provider_name",
    "gpu_id",
    "instance_or_offer_name",
    "observation_date",
    "price_usd_per_gpu_hour",
    "pricing_tier",
    "normalization_note",
    "source_url",
    "source_type",
    "source_confidence",
    "notes",
}

VALID_PROVIDER_IDS = {
    "prov000001", "prov000002", "prov000003", "prov000004", "prov000005",
    "prov000006", "prov000007", "prov000008", "prov000009",
}


def load_rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_builder_runs():
    result = subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "build_cloud_gpu_price_history.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "Wrote" in result.stdout


def test_builder_is_idempotent():
    # Running twice must not duplicate observations (ROWS is a static
    # hand-curated list; re-running just re-asserts the same rows).
    for _ in range(2):
        subprocess.run(
            [sys.executable, str(ROOT / "analytics" / "build_cloud_gpu_price_history.py")],
            cwd=ROOT,
            check=True,
        )

    rows = load_rows(CSV_PATH)
    ids = [row["observation_id"] for row in rows]
    assert len(ids) == len(set(ids))


def test_files_exist():
    assert CSV_PATH.exists()
    assert WAREHOUSE_PATH.exists()


def test_required_columns():
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        assert REQUIRED_COLUMNS.issubset(reader.fieldnames)


def test_provider_ids_reference_real_providers():
    for row in load_rows(CSV_PATH):
        assert row["provider_id"] in VALID_PROVIDER_IDS


def test_prices_are_positive_numbers():
    rows = load_rows(CSV_PATH)
    assert len(rows) >= 6
    for row in rows:
        assert float(row["price_usd_per_gpu_hour"]) > 0


def test_every_row_has_a_source_url():
    for row in load_rows(CSV_PATH):
        assert row["source_url"].startswith("https://")
