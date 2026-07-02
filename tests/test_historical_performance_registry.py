import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CSV_PATH = ROOT / "data" / "historical_performance_registry.csv"
WAREHOUSE_PATH = ROOT / "warehouse" / "historical" / "performance" / "historical_performance_registry.csv"

REQUIRED_COLUMNS = {
    "performance_record_id",
    "gpu_id",
    "vendor_registry",
    "vendor",
    "product_name",
    "peak_fp32_tflops",
    "peak_fp16_tflops",
    "sparsity_note",
    "memory_bandwidth_gbps",
    "memory_capacity_gb",
    "source_url",
    "source_type",
    "source_confidence",
    "notes",
}

VALID_SOURCE_CONFIDENCE = {"high", "medium", "low"}


def load_rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_builder_runs():
    result = subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "build_historical_performance_registry.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "Wrote" in result.stdout


def test_files_exist():
    assert CSV_PATH.exists()
    assert WAREHOUSE_PATH.exists()


def test_required_columns():
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        assert REQUIRED_COLUMNS.issubset(reader.fieldnames)


def test_unique_performance_record_ids():
    rows = load_rows(CSV_PATH)
    ids = [row["performance_record_id"] for row in rows]
    assert len(ids) == len(set(ids))


def test_source_confidence_is_governed():
    for row in load_rows(CSV_PATH):
        assert row["source_confidence"] in VALID_SOURCE_CONFIDENCE


def test_every_row_has_a_source_url():
    # Unlike pricing (where OEM-negotiated deals have no public price),
    # vendors do publish official/secondary spec pages for compute specs,
    # so every row should be traceable to a real page even when the
    # exact TFLOPS figure itself is left blank (see Gaudi2).
    for row in load_rows(CSV_PATH):
        assert row["source_url"].startswith("https://")


def test_gaudi2_deliberately_omits_unpublished_tflops():
    # Intel doesn't publish Gaudi2 compute performance in directly
    # comparable dense-TFLOPS terms; this registry leaves the field
    # blank rather than estimating it, unlike every other row which
    # has at least one TFLOPS figure.
    rows = load_rows(CSV_PATH)
    gaudi2 = next(row for row in rows if row["gpu_id"] == "intel-gaudi2")
    assert gaudi2["peak_fp32_tflops"] == ""
    assert gaudi2["peak_fp16_tflops"] == ""
    assert gaudi2["memory_bandwidth_gbps"] != ""


def test_covers_all_three_vendors():
    rows = load_rows(CSV_PATH)
    vendors = {row["vendor"] for row in rows}
    assert vendors == {"NVIDIA", "AMD", "Intel"}
