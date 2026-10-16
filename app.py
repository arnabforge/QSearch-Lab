import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from src.experiments import compare_search_algorithms
from src.grover_search import grover_search
from src.performance_analysis import generate_scaling_data


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="QSearch Lab",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==========================================================
# PAGE HEADER
# ==========================================================

st.title("⚛️ QSearch Lab")

st.subheader("Quantum vs Classical Search Performance Analysis")

st.markdown(
    """
    Explore classical linear search and Grover's quantum search
    through interactive experiments, circuit visualization,
    measurement analysis, and theoretical performance scaling.
    """
)

st.divider()


# ==========================================================
# SIDEBAR: EXPERIMENT CONFIGURATION
# ==========================================================

st.sidebar.title("⚙️ Experiment Configuration")

num_qubits = st.sidebar.slider(
    "Number of Qubits",
    min_value=2,
    max_value=6,
    value=4,
    step=1,
)

num_states = 2**num_qubits

target = st.sidebar.number_input(
    "Target State",
    min_value=0,
    max_value=num_states - 1,
    value=min(7, num_states - 1),
    step=1,
)

shots = st.sidebar.select_slider(
    "Measurement Shots",
    options=[128, 256, 512, 1024, 2048, 4096],
    value=1024,
)

noise_probability = st.sidebar.select_slider(
    "Depolarizing Noise Probability",
    options=[
        0.0,
        0.001,
        0.005,
        0.01,
        0.02,
        0.05,
        0.1,
    ],
    value=0.0,
    format_func=lambda value: f"{value:.1%}",
)

st.sidebar.caption(
    "This setting controls the simulated single-qubit "
    "gate-error probability. It is not a hardware noise measurement."
)

st.sidebar.info(
    f"Search space: {num_states} states\n\n"
    f"Binary target: {format(target, f'0{num_qubits}b')}"
)

run_experiment = st.sidebar.button(
    "Run Experiment 🚀",
    type="primary",
    use_container_width=True,
)


# ==========================================================
# RUN EXPERIMENT
# ==========================================================

if run_experiment:
    try:
        with st.spinner("Running quantum search simulations..."):

            # Classical-versus-quantum comparison.
            results = compare_search_algorithms(
                num_qubits=num_qubits,
                target=target,
                shots=shots,
                noise_probability=noise_probability,
            )

            # Obtain the circuit and detailed measurement results.
            quantum_details = grover_search(
                target=target,
                num_qubits=num_qubits,
                shots=shots,
                noise_probability=noise_probability,
            )

            # Run an ideal baseline using the same configuration.
            ideal_details = grover_search(
                target=target,
                num_qubits=num_qubits,
                shots=shots,
                noise_probability=0.0,
            )

            st.session_state["results"] = results
            st.session_state["quantum_details"] = quantum_details
            st.session_state["ideal_details"] = ideal_details

            st.session_state["experiment_config"] = {
                "num_qubits": num_qubits,
                "num_states": num_states,
                "target": target,
                "shots": shots,
                "noise_probability": noise_probability,
            }

    except Exception as error:
        st.error(f"Experiment failed: {error}")


# ==========================================================
# DISPLAY EXPERIMENT RESULTS
# ==========================================================

if "results" in st.session_state:

    results = st.session_state["results"]
    quantum_details = st.session_state["quantum_details"]
    ideal_details = st.session_state["ideal_details"]
    config = st.session_state["experiment_config"]

    classical = results["classical"]
    quantum = results["quantum"]

    experiment_target = config["target"]
    experiment_qubits = config["num_qubits"]
    experiment_states = config["num_states"]
    experiment_shots = config["shots"]
    experiment_noise = config["noise_probability"]

    st.success("Experiment completed successfully!")

    st.caption(
        f"Showing results for {experiment_qubits} qubits, "
        f"{experiment_states} states, target {experiment_target}, "
        f"{experiment_shots} shots, and "
        f"{experiment_noise:.1%} noise probability."
    )

    # ------------------------------------------------------
    # EXPERIMENT OVERVIEW
    # ------------------------------------------------------

    st.header("📊 Experiment Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Search Space", f"{results['num_states']} states")
    col2.metric("Classical Comparisons", classical["comparisons"])
    col3.metric("Grover Iterations", quantum["iterations"])
    col4.metric(
        "Noisy Target Probability",
        f"{quantum['target_probability']:.2%}",
    )

    st.divider()

    # ------------------------------------------------------
    # CLASSICAL VS QUANTUM
    # ------------------------------------------------------

    st.header("⚖️ Classical vs Quantum")

    left, right = st.columns(2)

    with left:
        st.subheader("🔍 Classical Linear Search")

        st.write(f"**Target found:** {classical['found']}")
        st.write(f"**Target index:** {classical['index']}")
        st.write(f"**Comparisons:** {classical['comparisons']}")

        st.write(
            f"**Measured runtime:** "
            f"{classical['runtime_seconds']:.6f} seconds"
        )

        st.caption(
            "Linear search has O(N) worst-case time complexity."
        )

    with right:
        st.subheader("⚛️ Quantum Grover Search")

        st.write(f"**Target:** {results['target']}")
        st.write(f"**Grover iterations:** {quantum['iterations']}")
        st.write(f"**Circuit depth:** {quantum['circuit_depth']}")
        st.write(f"**Gate count:** {quantum['gate_count']}")

        st.write(
            f"**Simulator runtime:** "
            f"{quantum['runtime_seconds']:.6f} seconds"
        )

        st.caption(
            "Grover's algorithm provides O(√N) oracle-query "
            "complexity for unstructured search with one marked target."
        )

    st.divider()

    # ------------------------------------------------------
    # IDEAL VS NOISY COMPARISON
    # ------------------------------------------------------

    st.header("🧪 Ideal vs Noisy Quantum Search")

    ideal_probability = ideal_details["target_probability"]
    noisy_probability = quantum_details["target_probability"]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Ideal Success Probability",
        f"{ideal_probability:.2%}",
    )

    col2.metric(
        "Noisy Success Probability",
        f"{noisy_probability:.2%}",
    )

    col3.metric(
        "Noise Probability",
        f"{experiment_noise:.1%}",
    )

    probability_difference = noisy_probability - ideal_probability

    st.write(
        f"Observed probability difference: "
        f"**{probability_difference:+.2%}**"
    )

    comparison_df = pd.DataFrame(
        {
            "Simulation": ["Ideal", "Noisy"],
            "Target Success Probability": [
                ideal_probability,
                noisy_probability,
            ],
        }
    )

    fig, ax = plt.subplots(figsize=(8, 4))

    bars = ax.bar(
        comparison_df["Simulation"],
        comparison_df["Target Success Probability"],
    )

    ax.set_title("Ideal vs Noisy Grover Search")
    ax.set_ylabel("Observed Target Success Probability")
    ax.set_ylim(0, 1.05)
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    ax.bar_label(
        bars,
        labels=[
            f"{value:.2%}"
            for value in comparison_df["Target Success Probability"]
        ],
        padding=3,
    )

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.caption(
        "Both simulations use the same target, qubit count, and shot count. "
        "The ideal and noisy simulations use separate random measurement "
        "samples, so observed differences can include sampling variation."
    )

    with st.expander("View probability comparison data"):
        st.dataframe(
            comparison_df,
            use_container_width=True,
            hide_index=True,
        )

    st.divider()

    # ------------------------------------------------------
    # QUANTUM MEASUREMENT DISTRIBUTION
    # ------------------------------------------------------

    st.header("📈 Quantum Measurement Distribution")

    counts = quantum_details["counts"]

    all_states = [
        format(state, f"0{experiment_qubits}b")
        for state in range(experiment_states)
    ]

    probabilities = {
        state: counts.get(state, 0) / experiment_shots
        for state in all_states
    }

    probability_df = pd.DataFrame(
        {
            "State": all_states,
            "Measurements": [
                counts.get(state, 0)
                for state in all_states
            ],
            "Probability": [
                probabilities[state]
                for state in all_states
            ],
        }
    )

    target_bitstring = format(
        experiment_target,
        f"0{experiment_qubits}b",
    )

    probability_df["Is Target"] = (
        probability_df["State"] == target_bitstring
    )

    fig, ax = plt.subplots(figsize=(12, 5))

    bar_colors = [
        "green" if state == target_bitstring else "steelblue"
        for state in probability_df["State"]
    ]

    ax.bar(
        probability_df["State"],
        probability_df["Probability"],
        color=bar_colors,
    )

    ax.set_title("Grover Search Measurement Probabilities")
    ax.set_xlabel("Measured Quantum State")
    ax.set_ylabel("Probability")
    ax.set_ylim(0, 1.05)
    ax.tick_params(axis="x", rotation=45)
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.caption(
        "Green represents the target state. Blue represents other states. "
        "States with zero measurements are also shown."
    )

    with st.expander("View measurement data"):
        st.dataframe(
            probability_df,
            use_container_width=True,
            hide_index=True,
        )

    st.divider()

    # ------------------------------------------------------
    # QUANTUM CIRCUIT
    # ------------------------------------------------------

    st.header("🔬 Quantum Circuit")

    st.code(
        quantum_details["circuit"].draw(output="text"),
        language="text",
    )

    circuit_col1, circuit_col2 = st.columns(2)

    circuit_col1.metric(
        "Circuit Depth",
        quantum_details["circuit_depth"],
    )

    circuit_col2.metric(
        "Total Gates",
        quantum_details["gate_count"],
    )

    st.divider()

    # ------------------------------------------------------
    # EXPORT EXPERIMENT RESULTS
    # ------------------------------------------------------

    st.header("📥 Export Experiment Results")

    export_df = pd.DataFrame(
        [
            {
                "Algorithm": "Classical Linear Search",
                "Search Space": results["num_states"],
                "Target": results["target"],
                "Comparisons": classical["comparisons"],
                "Grover Iterations": None,
                "Success Probability": None,
                "Noise Probability": None,
                "Runtime Seconds": classical["runtime_seconds"],
            },
            {
                "Algorithm": "Ideal Grover Search",
                "Search Space": results["num_states"],
                "Target": results["target"],
                "Comparisons": None,
                "Grover Iterations": ideal_details["iterations"],
                "Success Probability": ideal_probability,
                "Noise Probability": 0.0,
                "Runtime Seconds": None,
            },
            {
                "Algorithm": "Noisy Grover Search",
                "Search Space": results["num_states"],
                "Target": results["target"],
                "Comparisons": None,
                "Grover Iterations": quantum_details["iterations"],
                "Success Probability": noisy_probability,
                "Noise Probability": experiment_noise,
                "Runtime Seconds": quantum["runtime_seconds"],
            },
        ]
    )

    st.dataframe(
        export_df,
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        label="Download Experiment Results (CSV)",
        data=export_df.to_csv(index=False),
        file_name="qsearch_experiment_results.csv",
        mime="text/csv",
    )

    st.divider()

    # ------------------------------------------------------
    # SCIENTIFIC NOTE
    # ------------------------------------------------------

    st.subheader("🧪 Important Scientific Notes")

    st.info(
        """
        - Grover's algorithm provides a quadratic improvement in
          oracle-query complexity for unstructured search.
        - The noise model simulates depolarizing errors on selected
          single-qubit gates. It does not represent every physical
          quantum-device error.
        - Noise can affect the probability of measuring the target,
          but finite-shot sampling also causes variation between runs.
        - Simulator execution time is not evidence of quantum
          hardware speedup.
        """
    )

else:

    # ------------------------------------------------------
    # INITIAL PAGE
    # ------------------------------------------------------

    st.info(
        "Configure your experiment in the sidebar and click "
        "'Run Experiment' to begin."
    )

    st.markdown(
        """
        ### What you can explore

        - 🔍 Classical linear search
        - ⚛️ Grover's quantum search
        - 🧪 Ideal versus noisy quantum simulations
        - 📊 Quantum measurement probabilities
        - 🔬 Quantum-circuit structure
        - 📈 Theoretical query complexity
        - 📥 Downloadable experimental results
        """
    )


# ==========================================================
# PERFORMANCE SCALING ANALYSIS
# ==========================================================

st.divider()

st.header("📈 Performance Scaling Analysis")

st.markdown(
    """
    Compare the theoretical query complexity of classical
    linear search and Grover's quantum search as the search
    space increases.
    """
)

scaling_data = generate_scaling_data(
    min_qubits=2,
    max_qubits=10,
)

scaling_df = pd.DataFrame(scaling_data)

# ----------------------------------------------------------
# QUERY COMPLEXITY CHART
# ----------------------------------------------------------

st.subheader("Classical vs Quantum Query Complexity")

fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(
    scaling_df["Search Space"],
    scaling_df["Classical Worst-Case Comparisons"],
    marker="o",
    label="Classical Worst-Case Comparisons",
)

ax.plot(
    scaling_df["Search Space"],
    scaling_df["Grover Oracle Iterations"],
    marker="s",
    label="Grover Oracle Iterations",
)

ax.set_xlabel("Search Space Size (N)")
ax.set_ylabel("Comparisons / Oracle Iterations")
ax.set_title("Theoretical Search Complexity")
ax.set_xscale("log", base=2)
ax.set_yscale("log", base=2)
ax.grid(True, which="both", linestyle="--", alpha=0.3)
ax.legend()

fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.caption(
    "These curves show theoretical query counts, not execution times. "
    "The classical curve uses worst-case comparisons."
)

# ----------------------------------------------------------
# SCALING DATA TABLE
# ----------------------------------------------------------

st.subheader("📋 Performance Scaling Results")

st.dataframe(
    scaling_df,
    use_container_width=True,
    hide_index=True,
)

# ----------------------------------------------------------
# DOWNLOAD SCALING DATA
# ----------------------------------------------------------

st.download_button(
    label="Download Scaling Data (CSV)",
    data=scaling_df.to_csv(index=False),
    file_name="qsearch_scaling_data.csv",
    mime="text/csv",
)

# ----------------------------------------------------------
# COMPLEXITY EXPLANATION
# ----------------------------------------------------------

st.info(
    """
    **How to interpret this analysis**

    - Classical linear search requires up to N comparisons
      in the worst case.
    - Grover's algorithm requires approximately O(√N)
      oracle queries for unstructured search with one marked target.
    - The number of Grover iterations is an estimate for an
      ideal search problem with one marked state.
    - These are theoretical query-complexity estimates, not
      measured execution times or proof of hardware speedup.
    """
)