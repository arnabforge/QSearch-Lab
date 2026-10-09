import math


def calculate_grover_iterations(num_states: int) -> int:
    """Estimate Grover iterations for one marked target."""

    if num_states < 2:
        raise ValueError("num_states must be at least 2.")

    theta = math.asin(1 / math.sqrt(num_states))

    iterations = round(math.pi / (4 * theta) - 0.5)

    return max(0, iterations)


def generate_scaling_data(
    min_qubits: int = 2,
    max_qubits: int = 10,
) -> list[dict]:
    """Generate theoretical search complexity data."""

    if min_qubits < 1:
        raise ValueError("min_qubits must be at least 1.")

    if max_qubits < min_qubits:
        raise ValueError("Invalid qubit range.")

    results = []

    for num_qubits in range(min_qubits, max_qubits + 1):
        num_states = 2**num_qubits

        results.append({
            "Qubits": num_qubits,
            "Search Space": num_states,
            "Classical Worst-Case Comparisons": num_states,
            "Grover Oracle Iterations": (
                calculate_grover_iterations(num_states)
            ),
        })

    return results