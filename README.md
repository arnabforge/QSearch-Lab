# ⚛️ QSearch Lab

**An interactive quantum computing laboratory for comparing classical linear search with Grover's quantum search algorithm.**

QSearch Lab is a Python-based educational project that lets users configure a search problem, simulate Grover's algorithm, inspect measurement probabilities and circuit structure, and explore how theoretical query complexity scales as the search space grows.

## ✨ Features

- **Interactive experiment configuration** — choose the number of qubits, target state, and measurement shots.
- **Classical baseline** — run linear search and inspect the target index, number of comparisons, and measured runtime.
- **Grover's quantum search** — simulate Grover's algorithm and inspect its iteration count, target-state probability, circuit depth, gate count, and simulator runtime.
- **Measurement distribution** — visualize observed probabilities of measured quantum states and highlight the target state.
- **Circuit inspection** — display the generated quantum circuit in text form.
- **Performance scaling analysis** — compare theoretical classical worst-case comparisons with estimated Grover oracle iterations across increasing search-space sizes.
- **CSV export** — download experiment results for further analysis.
- **Automated tests** — run the project's test suite with `pytest`.

## 🖥️ Application Preview

The app includes an experiment overview, a classical-versus-quantum comparison, a measurement probability chart, a circuit view, and exportable results. Add screenshots of your running application here when ready.

Suggested screenshot paths:

```text
docs/
├── experiment-overview.png
├── measurement-distribution.png
└── performance-scaling.png
```

Once you add screenshots to `docs/`, you can display them in this section with Markdown, for example:

```markdown
![QSearch Lab experiment overview](docs/experiment-overview.png)
```

## 🧰 Tech Stack

- **Python**
- **Streamlit** — interactive web interface
- **Qiskit / Qiskit Aer** — quantum circuit construction and simulation (as used by the project dependencies)
- **Pandas** — tabular data and CSV export
- **Matplotlib** — visualizations
- **Pytest** — automated tests

## 📁 Project Structure

```text
QSearch-Lab/
├── app.py
├── main.py
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── classical_search.py
│   ├── experiments.py
│   ├── grover_search.py
│   └── performance_analysis.py
└── tests/
    ├── test_classical_search.py
    ├── test_experiments.py
    ├── test_grover_search.py
    └── test_performance_analysis.py
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/arnabforge/QSearch-Lab.git
cd QSearch-Lab
```

### 2. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use the environment's Python executable directly with the commands below, or follow your organization's PowerShell policy.

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## ▶️ Run the Application

From the project root, run:

```bash
streamlit run app.py
```

Streamlit will print a local address in the terminal (commonly `http://localhost:8501`). Open that address in your browser.

## 🧪 Run Tests

From the project root:

```bash
python -m pytest -v
```

To run an individual test file:

```bash
python -m pytest tests/test_grover_search.py -v
```

## 🔬 How to Use QSearch Lab

1. Start the Streamlit app.
2. Select the number of qubits in the sidebar. The search-space size is `N = 2ⁿ`, where `n` is the number of qubits.
3. Choose a target state within the valid range `0` to `N - 1`.
4. Select the number of measurement shots.
5. Click **Run Experiment**.
6. Compare the classical search results with Grover's search results.
7. Inspect the measurement distribution and quantum circuit.
8. Review the performance-scaling analysis and export results as CSV.

For example, with **4 qubits**, the search space contains **16 states**. Target state `7` is represented by the four-bit string `0111`. The ideal Grover circuit's success probability depends on the number of Grover iterations; the displayed measurement distribution is estimated from the simulation's measurement counts.

## 📈 Understanding the Results

- **Classical linear search:** has `O(N)` worst-case comparisons for a search space of size `N`.
- **Grover's algorithm:** provides `O(√N)` oracle-query complexity for unstructured search with one marked target, under the algorithm's assumptions.
- **Measurement probability:** the fraction of shots in which a state was observed.
- **Circuit depth and gate count:** describe aspects of the generated circuit, not the complete cost of running it on real quantum hardware.

### Scientific note

**Simulator runtime is not evidence of a quantum hardware speedup.** Classical and quantum timings can include different costs. Circuit construction, simulation, measurement, oracle implementation, and hardware execution must be considered separately. The performance-scaling chart shows theoretical query-complexity estimates, not measured execution-time comparisons.

## 📤 Exporting Results

Use the application's **Download Experiment Results (CSV)** button to save the current comparison. The performance-scaling section also provides a CSV download for its theoretical data.

## 🛠️ Troubleshooting

- **`ModuleNotFoundError` or unresolved imports:** activate the project's virtual environment and run `pip install -r requirements.txt`.
- **`streamlit` is not recognized:** run `python -m streamlit run app.py`.
- **Tests cannot import `pytest`:** install the dependencies from `requirements.txt`, then run `python -m pytest -v`.
- **VS Code still reports missing imports:** select the interpreter inside `.venv` using **Python: Select Interpreter**, then choose `.venv`.

## 🎯 Project Goal

QSearch Lab is intended as an educational tool for exploring the differences between classical search and Grover's quantum search through interactive experiments, quantum-circuit simulation, visualizations, and theoretical complexity analysis.

## 👤 Author

**Arnab De**  
GitHub: [@arnabforge](https://github.com/arnabforge)

## 📄 License

No license has been selected for this repository yet. If you intend to let others reuse, modify, or distribute the code, consider choosing an appropriate open-source license.
