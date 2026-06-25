import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analytics"))

from builders.join_utils import lookup, inner_join, require_keys


def test_lookup_returns_row():
    index = {
        "a": {"id": "a", "name": "Alpha"},
    }

    assert lookup(index, "a")["name"] == "Alpha"


def test_lookup_rejects_missing_key():
    with pytest.raises(KeyError):
        lookup({}, "missing")


def test_inner_join_matches_rows():
    left_rows = [
        {"id": "1", "ref": "a"},
        {"id": "2", "ref": "missing"},
    ]

    right_index = {
        "a": {"ref": "a", "name": "Alpha"},
    }

    joined = inner_join(left_rows, right_index, "ref")

    assert len(joined) == 1
    assert joined[0][0]["id"] == "1"
    assert joined[0][1]["name"] == "Alpha"


def test_require_keys_accepts_valid_rows():
    rows = [{"id": "1", "name": "Alpha"}]

    require_keys(rows, {"id", "name"})


def test_require_keys_rejects_missing_keys():
    rows = [{"id": "1"}]

    with pytest.raises(KeyError):
        require_keys(rows, {"id", "name"})
