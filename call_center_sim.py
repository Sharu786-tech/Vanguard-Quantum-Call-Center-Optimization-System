from pathlib import Path

import numpy as np
import pandas as pd


def estimate_service_level(calls, agents, avg_handle_time_minutes):
    hourly_capacity = agents * 60 / avg_handle_time_minutes
    utilization = calls / max(hourly_capacity, 1)

    if utilization <= 0.75:
        return 0.92
    if utilization <= 0.90:
        return 0.84
    if utilization <= 1.00:
        return 0.76
    if utilization <= 1.15:
        return 0.62
    return 0.45


def simulate_staffing_plan(input_path, output_path="data/simulation_results.csv", seed=101):
    rng = np.random.default_rng(seed)
    df = pd.read_csv(input_path, parse_dates=["timestamp"])

    actual_calls = []
    service_levels = []
    avg_wait_seconds = []

    for row in df.itertuples(index=False):
        calls = max(0, int(rng.normal(row.call_volume, max(row.call_volume * 0.08, 2))))
        service_level = estimate_service_level(
            calls,
            row.planned_agents,
            row.avg_handle_time_minutes,
        )
        wait_seconds = max(5, (1 - service_level) * 420)

        actual_calls.append(calls)
        service_levels.append(round(service_level, 3))
        avg_wait_seconds.append(round(wait_seconds, 1))

    df["simulated_actual_calls"] = actual_calls
    df["simulated_service_level"] = service_levels
    df["simulated_avg_wait_seconds"] = avg_wait_seconds
    df["meets_target"] = df["simulated_service_level"] >= df["service_level_target"]

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return df


if __name__ == "__main__":
    simulate_staffing_plan("data/staffing_plan.csv")
