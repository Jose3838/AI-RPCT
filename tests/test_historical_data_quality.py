import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
ANALYTICS = ROOT / "analytics"

sys.path.insert(0, str(ANALYTICS))

from historical_data_quality import (  # noqa: E402
    DataQualityError,
    validate_allowed_values,
    validate_https,
    validate_no_duplicate_rows,
    validate_not_empty,
    validate_references_exist,
    validate_required_columns,
    validate_unique,
)


def test_validate_not_empty_rejects_empty_rows():
    with pytest.raises(DataQualityError):
        validate_not_empty([])


def test_validate_required_columns_rejects_missing_column():
    rows = [{"id": "a"}]

    with pytest.raises(DataQualityError):
        validate_required_columns(rows, {"id", "name"})


def test_validate_unique_rejects_duplicate_values():
    rows = [{"id": "a"}, {"id": "a"}]

    with pytest.raises(DataQualityError):
        validate_unique(rows, "id")


def test_validate_allowed_values_rejects_invalid_values():
    rows = [{"status": "unknown"}]

    with pytest.raises(DataQualityError):
        validate_allowed_values(rows, "status", {"active"})


def test_validate_https_rejects_non_https_values():
    rows = [{"url": "http://example.com"}]

    with pytest.raises(DataQualityError):
        validate_https(rows, "url")


def test_validate_no_duplicate_rows_rejects_duplicates():
    rows = [{"id": "a", "name": "Alpha"}, {"id": "a", "name": "Alpha"}]

    with pytest.raises(DataQualityError):
        validate_no_duplicate_rows(rows)


def test_validate_references_exist_rejects_unknown_reference():
    rows = [{"source_id": "unknown"}]

    with pytest.raises(DataQualityError):
        validate_references_exist(rows, "source_id", {"known"})


def test_generic_registry_validator_runs():
    result = subprocess.run(
        [sys.executable, str(ROOT / "analytics" / "validate_registry.py")],
        cwd=ROOT / "analytics",
        text=True,
        capture_output=True,
        check=True,
    )

    assert "Historical registry validation passed" in result.stdout
