from copilot.service import get_why


def test_get_why():
    result = get_why()

    assert isinstance(result, dict)

    assert "decision" in result or "status" in result
