import math

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error


def grover_search(
    target: int,
    num_qubits: int = 4,
    shots: int = 1024,
    noise_probability: float = 0.0,
):
    """
    Search for a target state using Grover's algorithm.

    Args:
        target: Integer representing the target state.
        num_qubits: Number of qubits in the search circuit.
        shots: Number of measurement repetitions.
        noise_probability: Depolarizing gate-error probability,
            between 0 and 1.

    Returns:
        Dictionary containing measurement counts and circuit metrics.
    """

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

    iterations = max(
        0,
        round((math.pi / 4) * math.sqrt(num_states) - 0.5),
    )

    circuit = QuantumCircuit(num_qubits, num_qubits)

    # Create an equal superposition.
    circuit.h(range(num_qubits))

    # Apply Grover iterations.
    for _ in range(iterations):

        # Oracle: Flip the phase of the target state.
        for qubit in range(num_qubits):
            if (target >> qubit) & 1 == 0:
                circuit.x(qubit)

        circuit.h(num_qubits - 1)
        circuit.mcx(
            list(range(num_qubits - 1)),
            num_qubits - 1,
        )
        circuit.h(num_qubits - 1)

        for qubit in range(num_qubits):
            if (target >> qubit) & 1 == 0:
                circuit.x(qubit)

        # Diffusion operator.
        circuit.h(range(num_qubits))
        circuit.x(range(num_qubits))

        circuit.h(num_qubits - 1)
        circuit.mcx(
            list(range(num_qubits - 1)),
            num_qubits - 1,
        )
        circuit.h(num_qubits - 1)

        circuit.x(range(num_qubits))
        circuit.h(range(num_qubits))

    # Measure the qubits.
    circuit.measure(range(num_qubits), range(num_qubits))

    # Configure the simulator.
    if noise_probability == 0.0:
        simulator = AerSimulator()
    else:
        noise_model = NoiseModel()

        error = depolarizing_error(
            noise_probability,
            1,
        )

        # Apply the error to single-qubit gates after transpilation.
        noise_model.add_all_qubit_quantum_error(
            error,
            ["h", "x"],
        )

        simulator = AerSimulator(noise_model=noise_model)

    compiled_circuit = transpile(circuit, simulator)

    result = simulator.run(
        compiled_circuit,
        shots=shots,
    ).result()

    counts = result.get_counts()

    target_state = format(target, f"0{num_qubits}b")
    target_probability = counts.get(target_state, 0) / shots

    return {
        "target": target,
        "num_qubits": num_qubits,
        "num_states": num_states,
        "iterations": iterations,
        "shots": shots,
        "noise_probability": noise_probability,
        "counts": counts,
        "target_probability": target_probability,
        "circuit_depth": compiled_circuit.depth(),
        "gate_count": compiled_circuit.size(),
        "circuit": circuit,
    }