import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CSV_PATH = ROOT / "data" / "historical_pricing_registry.csv"
WAREHOUSE_PATH = ROOT / "warehouse" / "historical" / "pricing" / "historical_pricing_registry.csv"

REQUIRED_COLUMNS = {
    "pricing_record_id",
    "relationship_id",
    "observation_date",
    "price_amount",
    "currency",
    "unit",
    "price_type",
    "verification_status",
    "source_id",
    "notes",
}


def load_rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_builder_runs():
    result = subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "build_historical_pricing_registry.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "Wrote" in result.stdout


def test_files_exist():
    assert CSV_PATH.exists()
    assert WAREHOUSE_PATH.exists()


def test_required_columns_even_when_empty():
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        assert REQUIRED_COLUMNS.issubset(reader.fieldnames)


def test_pricing_registry_v2_has_nvidia_anchor_points():
    # v1 shipped intentionally empty (no verifiable price data yet).
    # v2 adds a small number of NVIDIA data-center GPU price points where
    # public reporting gives a reasonable (if not officially confirmed)
    # anchor. AMD Instinct and Intel Gaudi/Data Center GPU Max are
    # deliberately still absent — no credible public list price exists
    # for those (enterprise-only, OEM-negotiated pricing) and this
    # registry does not fabricate figures it can't reasonably back.
    rows = load_rows(CSV_PATH)
    assert len(rows) == 4

    for row in rows:
        assert row["verification_status"] == "partial"
        assert row["source_id"] == "market_reporting_estimate"
        assert float(row["price_amount"]) > 0


def test_pricing_registry_does_not_fabricate_amd_or_intel_prices():
    rows = load_rows(CSV_PATH)
    priced_gpu_ids = {row["relationship_id"] for row in rows}
    # rel000011-014 are the NVIDIA priced_by relationships added alongside
    # this registry; nothing else should be priced yet.
    assert priced_gpu_ids == {"rel000011", "rel000012", "rel000013", "rel000014"}
