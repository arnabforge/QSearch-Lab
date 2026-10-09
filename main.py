from src.experiments import compare_search_algorithms


def main():
    results = compare_search_algorithms(
        num_qubits=4,
        target=7,
        shots=1024,
    )

    classical = results["classical"]
    quantum = results["quantum"]

    print("\n" + "=" * 45)
    print("       QSEARCH LAB")
    print("  CLASSICAL VS QUANTUM SEARCH")
    print("=" * 45)

    print(f"\nSearch space: {results['num_states']} states")
    print(f"Target: {results['target']}")

    print("\n--- CLASSICAL LINEAR SEARCH ---")
    print(f"Found: {classical['found']}")
    print(f"Index: {classical['index']}")
    print(f"Comparisons: {classical['comparisons']}")
    print(f"Runtime: {classical['runtime_seconds']:.6f} seconds")

    print("\n--- QUANTUM GROVER SEARCH ---")
    print(f"Grover iterations: {quantum['iterations']}")
    print(
        f"Target probability: "
        f"{quantum['target_probability']:.2%}"
    )
    print(f"Circuit depth: {quantum['circuit_depth']}")
    print(f"Gate count: {quantum['gate_count']}")
    print(f"Runtime: {quantum['runtime_seconds']:.6f} seconds")

    print("\n--- EXPERIMENT SUMMARY ---")
    print(
        "Classical comparisons:",
        classical["comparisons"],
    )
    print(
        "Quantum oracle iterations:",
        quantum["iterations"],
    )

    print("\nNote: These are algorithm and simulator measurements.")
    print("They do not establish a real quantum hardware speedup.")


if __name__ == "__main__":
    main()