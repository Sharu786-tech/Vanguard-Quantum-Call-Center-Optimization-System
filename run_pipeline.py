from data.generate_sample_data import generate_sample_data
from forecasting.forecast_calls import forecast_call_volume
from optimization.staffing_qubo import build_staffing_plan
from simulation.call_center_sim import simulate_staffing_plan


def main():
    raw_path = "data/call_center_sample.csv"
    forecast_path = "data/forecast_output.csv"
    staffing_path = "data/staffing_plan.csv"
    simulation_path = "data/simulation_results.csv"

    generate_sample_data(raw_path)
    forecast_call_volume(raw_path, forecast_path)
    build_staffing_plan(forecast_path, staffing_path)
    simulate_staffing_plan(staffing_path, simulation_path)

    print("Pipeline complete.")
    print(f"Forecast: {forecast_path}")
    print(f"Staffing plan: {staffing_path}")
    print(f"Simulation results: {simulation_path}")


if __name__ == "__main__":
    main()
