import pytest

from src.grover_search import grover_search


def test_grover_finds_target():
    result = grover_search(
        target=7,
        num_qubits=4,
        shots=1024
    )

    assert result["target"] == 7
    assert result["num_states"] == 16
    assert result["target_probability"] > 0.90


def test_grover_supports_different_targets():
    result = grover_search(
        target=12,
        num_qubits=4,
        shots=1024
    )

    assert result["target"] == 12
    assert result["target_probability"] > 0.90


def test_invalid_target_raises_error():
    with pytest.raises(ValueError):
        grover_search(
            target=16,
            num_qubits=4
        )


def test_invalid_qubit_count_raises_error():
    with pytest.raises(ValueError):
        grover_search(
            target=0,
            num_qubits=0
        )