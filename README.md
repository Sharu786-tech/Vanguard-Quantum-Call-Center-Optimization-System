# Vanguard Call Center Quantum Optimization

This project demonstrates a hybrid quantum-classical workflow for call center planning.
It forecasts incoming call volume, converts staffing decisions into a QUBO-style
optimization problem, solves the schedule with a classical fallback solver, and
simulates service quality.

The use case is inspired by a large investment firm call center where demand changes
by hour, day, market conditions, and client activity. The goal is to minimize staffing
cost while meeting service-level targets.

## Project Structure

```text
vanguard_call_center_quantum/
├── data/
├── notebooks/
├── forecasting/
├── optimization/
├── qaoa/
├── simulation/
├── dashboard/
├── report/
├── presentation/
└── README.md
```

## Quick Start

Install dependencies:

```bash
pip install -r requirements.txt
```

Generate data and run the workflow:

```bash
python run_pipeline.py
```

Start the dashboard:

```bash
streamlit run dashboard/app.py
```

## Core Idea

For each planning hour, the system chooses a staffing level.

```text
Minimize:
  staffing_cost
  + under_staffing_penalty
  + over_staffing_penalty
  + service_level_penalty
```

The optimization can be represented as a QUBO problem:

```text
minimize x^T Q x
```

where each binary variable represents a staffing choice for a specific hour.

## Outputs

The pipeline creates:

- `data/call_center_sample.csv`
- `data/forecast_output.csv`
- `data/staffing_plan.csv`
- `data/simulation_results.csv`

## Notes

The QAOA module is written as a clean extension point. If Qiskit is installed, you can
replace the placeholder solver with a real QAOA backend. The default project stays
lightweight and runs locally with standard Python packages.
