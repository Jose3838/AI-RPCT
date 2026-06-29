import csv

from copilot import executive_snapshot_repository
from copilot import executive_snapshot_writer


def test_write_executive_snapshot_writes_registry_row(tmp_path, monkeypatch):
    output = tmp_path / "data" / "executive_snapshot_registry.csv"

    monkeypatch.setattr(
        executive_snapshot_repository,
        "ROOT",
        tmp_path,
    )

    snapshot = executive_snapshot_writer.write_executive_snapshot()

    assert output.exists()

    with output.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == 1
    assert rows[0]["snapshot_id"] == snapshot["snapshot_id"]
    assert rows[0]["risk_score"] == str(snapshot["risk_score"])
    assert rows[0]["risk_severity"] == snapshot["risk_severity"]
    assert rows[0]["recommendation"] == snapshot["recommendation"]
    assert rows[0]["source"] == "executive_snapshot_builder"
