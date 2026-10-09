from src.classical_search import linear_search


def test_target_found():
    result = linear_search([10, 20, 30, 40], 30)

    assert result["found"] is True
    assert result["index"] == 2
    assert result["comparisons"] == 3


def test_target_not_found():
    result = linear_search([10, 20, 30], 50)

    assert result["found"] is False
    assert result["index"] == -1
    assert result["comparisons"] == 3


def test_target_at_first_position():
    result = linear_search([10, 20, 30], 10)

    assert result["found"] is True
    assert result["index"] == 0
    assert result["comparisons"] == 1


def test_empty_collection():
    result = linear_search([], 10)

    assert result["found"] is False
    assert result["index"] == -1
    assert result["comparisons"] == 0