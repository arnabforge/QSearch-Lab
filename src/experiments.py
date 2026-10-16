from time import perf_counter

from src.classical_search import linear_search
from src.grover_search import grover_search


def compare_search_algorithms(
    num_qubits: int = 4,
    target: int = 7,
    shots: int = 1024,
    noise_probability: float = 0.0,
) -> dict:
    """
    Compare classical linear search with Grover's quantum search.

    Args:
        num_qubits: Number of qubits in the search circuit.
        target: Integer representing the target state.
        shots: Number of measurement repetitions.
        noise_probability: Depolarizing gate-error probability
            between 0 and 1. Defaults to 0.0 (ideal simulation).

    Returns:
        Dictionary containing classical and quantum search results.

    Note:
        Runtime measurements include the work performed by each
        implementation. They should not be interpreted as a direct
        comparison of classical and quantum hardware speed.
    """

    # Validate inputs.
    if num_qubits < 1:
        raise ValueError("num_qubits must be at least 1.")

    if shots < 1:
        raise ValueError("shots must be at least 1.")

    if not 0.0 <= noise_probability <= 1.0:
        raise ValueError(
            "noise_probability must be between 0 and 1."
        )

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
        noise_probability=noise_probability,
    )

    quantum_time = perf_counter() - start_time

    # Return comparison results.
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
            "noise_probability": quantum_result["noise_probability"],
        },
    }