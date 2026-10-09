import pytest

from src.experiments import compare_search_algorithms


def test_comparison_returns_both_results():
    result = compare_search_algorithms(
        num_qubits=3,
        target=5,
        shots=512,
    )

    assert result["num_states"] == 8
    assert result["target"] == 5

    assert result["classical"]["found"] is True
    assert result["classical"]["index"] == 5

    assert 0 <= result["quantum"]["target_probability"] <= 1


def test_comparison_rejects_invalid_target():
    with pytest.raises(ValueError):
        compare_search_algorithms(
            num_qubits=3,
            target=8,
        )


def test_comparison_rejects_invalid_qubit_count():
    with pytest.raises(ValueError):
        compare_search_algorithms(
            num_qubits=0,
            target=0,
        )