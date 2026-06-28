from copilot.service import (
    get_analytics,
    get_context,
    get_decision,
    get_decision_intelligence,
    get_decision_timeline,
    get_recommendation,
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


def test_get_decision_intelligence():
    result = get_decision_intelligence()

    assert isinstance(result, dict)
    assert "summary" in result or "status" in result

    if "summary" in result:
        assert "metrics" in result
        assert "trends" in result
        assert "insights" in result

        assert result["summary"]["decision_count"] >= 1

        assert "recommendation_count" in result["metrics"]
        assert "recommendation_consistency" in result["metrics"]

        assert isinstance(result["trends"], dict)
        assert isinstance(result["insights"], list)
