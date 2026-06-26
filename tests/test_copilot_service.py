from copilot.service import (
    get_context,
    get_decision,
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
