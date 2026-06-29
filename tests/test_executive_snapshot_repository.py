from copilot.executive_snapshot_repository import (
    get_latest_executive_snapshot,
    load_executive_snapshot_rows,
)


def test_load_executive_snapshot_rows():
    rows = load_executive_snapshot_rows()

    assert isinstance(rows, list)
    assert rows

    assert "snapshot_id" in rows[0]
    assert "risk_score" in rows[0]
    assert "risk_severity" in rows[0]


def test_get_latest_executive_snapshot():
    snapshot = get_latest_executive_snapshot()

    assert snapshot is not None

    assert "snapshot_id" in snapshot
    assert "generated_at" in snapshot
    assert "risk_score" in snapshot
    assert "risk_severity" in snapshot
