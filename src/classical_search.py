from typing import Any, Sequence


def linear_search(data: Sequence[Any], target: Any) -> dict:
    """
    Search for a target using classical linear search.

    Returns:
        A dictionary containing:
        - found: whether the target exists
        - index: target index, or -1 if not found
        - comparisons: number of elements checked
    """

    comparisons = 0

    for index, value in enumerate(data):
        comparisons += 1

        if value == target:
            return {
                "found": True,
                "index": index,
                "comparisons": comparisons,
            }

    return {
        "found": False,
        "index": -1,
        "comparisons": comparisons,
    }