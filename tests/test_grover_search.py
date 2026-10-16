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

def test_grover_search_accepts_noise_probability():
    result = grover_search(
        target=7,
        num_qubits=4,
        shots=1024,
        noise_probability=0.05,
    )

    assert result["noise_probability"] == 0.05
    assert 0.0 <= result["target_probability"] <= 1.0


def test_grover_search_rejects_invalid_noise_probability():
    import pytest

    with pytest.raises(ValueError):
        grover_search(
            target=7,
            num_qubits=4,
            shots=1024,
            noise_probability=1.5,
        )