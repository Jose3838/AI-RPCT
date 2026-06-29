from copilot import executive_snapshot_scheduler


def test_run_executive_snapshot(monkeypatch):
    expected_snapshot = {
        "snapshot_id": "snapshot-test",
        "generated_at": "2026-06-29T00:00:00+00:00",
        "risk_score": 100,
        "risk_severity": "low",
        "recommendation": "Continue monitoring current infrastructure.",
        "source": "executive_snapshot_builder",
    }

    monkeypatch.setattr(
        executive_snapshot_scheduler,
        "write_executive_snapshot",
        lambda: expected_snapshot,
    )

    result = executive_snapshot_scheduler.run_executive_snapshot()

    assert result["status"] == "executive snapshot completed"
    assert result["snapshot"] == expected_snapshot
