import math

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def grover_search(target: int, num_qubits: int = 4, shots: int = 1024):
    """
    Search for a target state using Grover's algorithm.

    Args:
        target: Integer representing the target state.
        num_qubits: Number of qubits in the search circuit.
        shots: Number of measurement repetitions.

    Returns:
        Dictionary containing measurement counts and circuit metrics.
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

    # Calculate the number of Grover iterations.
    iterations = max(
        0,
        round((math.pi / 4) * math.sqrt(num_states) - 0.5)
    )

    # Create the quantum circuit.
    circuit = QuantumCircuit(num_qubits, num_qubits)

    # Step 1: Create an equal superposition.
    circuit.h(range(num_qubits))

    # Step 2: Apply Grover iterations.
    for _ in range(iterations):

        # Oracle: Flip the phase of the target state.
        for qubit in range(num_qubits):
            if (target >> qubit) & 1 == 0:
                circuit.x(qubit)

        circuit.h(num_qubits - 1)
        circuit.mcx(
            list(range(num_qubits - 1)),
            num_qubits - 1
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
            num_qubits - 1
        )
        circuit.h(num_qubits - 1)

        circuit.x(range(num_qubits))
        circuit.h(range(num_qubits))

    # Step 3: Measure the qubits.
    circuit.measure(range(num_qubits), range(num_qubits))

    # Step 4: Simulate the circuit.
    simulator = AerSimulator()
    compiled_circuit = transpile(circuit, simulator)

    result = simulator.run(
        compiled_circuit,
        shots=shots
    ).result()

    counts = result.get_counts()

    # Convert the target to Qiskit's bit-string representation.
    target_state = format(target, f"0{num_qubits}b")

    target_probability = counts.get(target_state, 0) / shots

    return {
        "target": target,
        "num_qubits": num_qubits,
        "num_states": num_states,
        "iterations": iterations,
        "shots": shots,
        "counts": counts,
        "target_probability": target_probability,
        "circuit_depth": compiled_circuit.depth(),
        "gate_count": compiled_circuit.size(),
        "circuit": circuit,
    }