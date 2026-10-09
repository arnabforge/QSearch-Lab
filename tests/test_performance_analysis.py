import pytest

from src.performance_analysis import (
    calculate_grover_iterations,
    generate_scaling_data,
)


def test_grover_iterations_for_four_states():
    assert calculate_grover_iterations(4) == 1


def test_grover_iterations_for_sixteen_states():
    assert calculate_grover_iterations(16) == 3


def test_scaling_data():
    data = generate_scaling_data(2, 4)

    assert len(data) == 3
    assert data[0]["Search Space"] == 4
    assert data[1]["Search Space"] == 8
    assert data[2]["Search Space"] == 16


def test_invalid_search_space():
    with pytest.raises(ValueError):
        calculate_grover_iterations(1)


def test_invalid_qubit_range():
    with pytest.raises(ValueError):
        generate_scaling_data(5, 2)