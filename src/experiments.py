from time import perf_counter

from src.classical_search import linear_search
from src.grover_search import grover_search


def compare_search_algorithms(
    num_qubits: int = 4,
    target: int = 7,
    shots: int = 1024,
) -> dict:
    """
    Compare classical linear search with Grover's quantum search.

    Runtime measurements include the work performed by each
    implementation, so they should not be interpreted as a
    direct comparison of classical and quantum hardware speed.
    """

    if num_qubits < 1:
        raise ValueError("num_qubits must be at least 1.")

    if shots < 1:
        raise ValueError("shots must be at least 1.")

    num_states = 2**num_qubits

    if not 0 <= target < num_states:
        raise ValueError(
            f"Target must be between 0 and {num_states - 1}."
        )

    # Build the classical search space.
    data = list(range(num_states))

    # Run classical linear search.
    start_time = perf_counter()

    classical_result = linear_search(data, target)

    classical_time = perf_counter() - start_time

    # Run Grover's quantum search.
    start_time = perf_counter()

    quantum_result = grover_search(
        target=target,
        num_qubits=num_qubits,
        shots=shots,
    )

    quantum_time = perf_counter() - start_time

    return {
        "num_states": num_states,
        "target": target,
        "classical": {
            **classical_result,
            "runtime_seconds": classical_time,
        },
        "quantum": {
            "iterations": quantum_result["iterations"],
            "target_probability": quantum_result["target_probability"],
            "circuit_depth": quantum_result["circuit_depth"],
            "gate_count": quantum_result["gate_count"],
            "runtime_seconds": quantum_time,
            "measurement_counts": quantum_result["counts"],
        },
    }