from copilot.executive_snapshot_builder import build_executive_snapshot
from copilot.service import (
    get_analytics,
    get_capacity_intelligence,
    get_change_intelligence,
    get_context,
    get_decision,
    get_decision_intelligence,
    get_decision_timeline,
    get_executive_intelligence,
    get_executive_snapshots,
    get_forecast_intelligence,
    get_provider_intelligence,
    get_recommendation,
    get_risk_intelligence,
    get_status,
    get_summary,
    get_why,
)

def test_get_why():
    result = get_why()

    assert isinstance(result, dict)
    assert "decision" in result or "status" in result


def test_get_status():
    result = get_status()

    assert result["platform_status"] == "healthy"
    assert result["pipeline"] == "ok"
    assert result["decision_engine"] == "ok"


def test_get_decision():
    result = get_decision()

    assert isinstance(result, dict)
    assert "decision" in result or "status" in result

    if "decision" in result:
        assert "confidence" in result
        assert "topic" in result
        assert "generated_at" in result


def test_get_summary():
    result = get_summary()

    assert isinstance(result, dict)
    assert "summary" in result or "status" in result


def test_get_context():
    result = get_context()

    assert isinstance(result, dict)
    assert "platform_status" in result
    assert "pipeline" in result
    assert "decision" in result
    assert "confidence" in result


def test_get_recommendation():
    result = get_recommendation()

    assert isinstance(result, dict)
    assert "recommendation_score" in result or "status" in result

    if "recommendation_score" in result:
        assert 0 <= result["recommendation_score"] <= 100
        assert result["priority"] in {"high", "medium", "low"}
        assert "priority_reason" in result
        assert result["priority_reason"]


def test_get_decision_timeline():
    result = get_decision_timeline()

    assert isinstance(result, dict)
    assert "timeline" in result or "status" in result

    if "timeline" in result:
        assert "count" in result
        assert "returned" in result
        assert isinstance(result["timeline"], list)


def test_get_analytics():
    result = get_analytics()

    assert isinstance(result, dict)
    assert "decision_count" in result or "status" in result

    if "decision_count" in result:
        assert result["decision_count"] >= 1
        assert 0 <= result["average_confidence"] <= 1
        assert 0 <= result["min_confidence"] <= 1
        assert 0 <= result["max_confidence"] <= 1


def test_get_forecast_intelligence():
    result = get_forecast_intelligence()

    assert isinstance(result, dict)
    assert "summary" in result or "status" in result

    if "summary" in result:
        assert "metrics" in result
        assert "trends" in result
        assert "insights" in result

        assert result["summary"]["forecast_count"] >= 1

        assert isinstance(result["metrics"], dict)
        assert isinstance(result["trends"], dict)
        assert isinstance(result["insights"], list)

        assert result["insights"]
        assert "type" in result["insights"][0]
        assert "severity" in result["insights"][0]
        assert "message" in result["insights"][0]


def test_get_decision_intelligence():
    result = get_decision_intelligence()

    assert isinstance(result, dict)
    assert "summary" in result or "status" in result

    if "summary" in result:
        assert "metrics" in result
        assert "trends" in result
        assert "insights" in result

        assert result["summary"]["decision_count"] >= 1
        assert "latest_decision" in result["summary"]

        assert "recommendation_count" in result["metrics"]
        assert "recommendation_consistency" in result["metrics"]

        assert isinstance(result["trends"], dict)
        assert isinstance(result["insights"], list)

        assert result["insights"]
        assert "type" in result["insights"][0]
        assert "severity" in result["insights"][0]
        assert "message" in result["insights"][0]


def test_get_provider_intelligence():
    result = get_provider_intelligence()

    assert isinstance(result, dict)
    assert "summary" in result or "status" in result

    if "summary" in result:
        assert "metrics" in result
        assert "trends" in result
        assert "insights" in result

        assert result["summary"]["provider_count"] >= 1
        assert result["summary"]["active_provider_count"] >= 1

        assert "provider_categories" in result["metrics"]
        assert isinstance(result["metrics"]["provider_categories"], dict)

        assert isinstance(result["trends"], dict)
        assert isinstance(result["insights"], list)

        assert result["insights"]
        assert "type" in result["insights"][0]
        assert "severity" in result["insights"][0]
        assert "message" in result["insights"][0]


def test_get_capacity_intelligence():
    result = get_capacity_intelligence()

    assert isinstance(result, dict)
    assert "summary" in result or "status" in result

    if "summary" in result:
        assert "metrics" in result
        assert "trends" in result
        assert "insights" in result

        assert result["summary"]["capacity_records"] >= 1

        assert "capacity_status" in result["metrics"]
        assert "availability_levels" in result["metrics"]

        assert isinstance(result["metrics"]["capacity_status"], dict)
        assert isinstance(result["metrics"]["availability_levels"], dict)
        assert isinstance(result["trends"], dict)
        assert isinstance(result["insights"], list)

        assert result["insights"]
        assert "type" in result["insights"][0]
        assert "severity" in result["insights"][0]
        assert "message" in result["insights"][0]


def test_get_risk_intelligence():
    result = get_risk_intelligence()

    assert isinstance(result, dict)
    assert "summary" in result
    assert "metrics" in result
    assert "trends" in result
    assert "insights" in result

    assert result["summary"]["status"] == "risk intelligence available"

    assert result["metrics"]["provider_count"] >= 1
    assert result["metrics"]["capacity_records"] >= 1
    assert result["metrics"]["forecast_records"] >= 1
    assert result["metrics"]["provider_risk"] in {"low", "high"}
    assert result["metrics"]["capacity_risk"] in {"low", "high"}
    assert result["metrics"]["forecast_risk"] in {"low", "high"}

    assert isinstance(result["trends"], dict)
    assert isinstance(result["insights"], list)
    assert result["insights"]

    assert "type" in result["insights"][0]
    assert "severity" in result["insights"][0]
    assert "message" in result["insights"][0]

    assert "risk_score" in result["summary"]
    assert 0 <= result["summary"]["risk_score"] <= 100

    assert "risk_severity" in result["summary"]
    assert "recommendation" in result["summary"]
    assert result["summary"]["recommendation"]
    assert result["summary"]["risk_severity"] in {
        "low",
        "medium",
        "high",
        "critical",
    }

    assert (
        result["insights"][0]["severity"]
        == result["summary"]["risk_severity"]
    )

def test_get_executive_intelligence():
    result = get_executive_intelligence()

    assert isinstance(result, dict)

    assert "summary" in result
    assert "modules" in result

    assert (
        result["summary"]["status"]
        == "executive intelligence available"
    )

    modules = result["modules"]

    assert "summary" in modules
    assert "analytics" in modules
    assert "decision_intelligence" in modules
    assert "forecast_intelligence" in modules
    assert "provider_intelligence" in modules
    assert "capacity_intelligence" in modules
    assert "risk_intelligence" in modules

    assert isinstance(modules, dict)

    assert "generated_at" in result["summary"]
    assert "overall_risk_score" in result["summary"]
    assert "overall_risk_severity" in result["summary"]
    assert "overall_recommendation" in result["summary"]

def test_get_change_intelligence():
    result = get_change_intelligence()

    assert isinstance(result, dict)

    assert "summary" in result
    assert "metrics" in result
    assert "changes" in result
    assert "insights" in result

    assert (
        result["summary"]["status"]
        == "change intelligence available"
    )

    assert "baseline" in result["summary"]

    assert "risk_score" in result["metrics"]
    assert "risk_severity" in result["metrics"]

    assert isinstance(result["changes"], list)
    assert isinstance(result["insights"], list)

    assert result["insights"]
    assert "type" in result["insights"][0]
    assert "severity" in result["insights"][0]
    assert "message" in result["insights"][0]

def test_get_executive_snapshots():
    result = get_executive_snapshots()

    assert isinstance(result, dict)

    assert "summary" in result
    assert "snapshots" in result

    assert (
        result["summary"]["status"]
        == "executive snapshots available"
    )

    assert result["summary"]["snapshot_count"] >= 1
    assert "latest_snapshot" in result["summary"]

    assert isinstance(result["snapshots"], list)
    assert result["snapshots"]

    latest = result["summary"]["latest_snapshot"]

    assert "snapshot_id" in latest
    assert "generated_at" in latest
    assert "risk_score" in latest
    assert "risk_severity" in latest
    assert "recommendation" in latest

def test_build_executive_snapshot():
    snapshot = build_executive_snapshot()

    assert isinstance(snapshot, dict)

    assert "snapshot_id" in snapshot
    assert "generated_at" in snapshot
    assert "risk_score" in snapshot
    assert "risk_severity" in snapshot
    assert "recommendation" in snapshot
    assert "source" in snapshot

    assert snapshot["snapshot_id"].startswith("snapshot-")
    assert 0 <= snapshot["risk_score"] <= 100
    assert snapshot["risk_severity"] in {
        "low",
        "medium",
        "high",
        "critical",
    }
    assert snapshot["source"] == "executive_snapshot_builder"
