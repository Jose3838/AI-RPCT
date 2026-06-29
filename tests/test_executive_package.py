from copilot.executive.recommendation import (
    get_executive_recommendation,
)


def test_executive_package_import():
    result = get_executive_recommendation()

    assert isinstance(result, dict)
    assert "summary" in result
    assert "recommendation" in result
