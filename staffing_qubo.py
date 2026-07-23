from pathlib import Path

import numpy as np
import pandas as pd


def required_agents(calls, avg_handle_time_minutes, occupancy_target=0.82):
    workload_minutes = calls * avg_handle_time_minutes
    available_minutes_per_agent = 60 * occupancy_target
    return int(np.ceil(workload_minutes / available_minutes_per_agent))


def score_staffing_choice(
    agents,
    required,
    hourly_agent_cost=42,
    understaff_penalty=600,
    overstaff_penalty=55,
):
    understaffed = max(0, required - agents)
    overstaffed = max(0, agents - required)
    return (
        agents * hourly_agent_cost
        + understaffed * understaff_penalty
        + overstaffed * overstaff_penalty
    )


def solve_hour_classically(required, min_agents=1, max_agents=90):
    candidates = range(min_agents, max_agents + 1)
    return min(candidates, key=lambda agents: score_staffing_choice(agents, required))


def build_qubo_for_hour(required, max_agents=90):
    """Build a one-hot QUBO where one binary variable selects one staffing level."""
    penalty = 10_000
    qubo = {}

    def add(i, j, value):
        key = tuple(sorted((i, j)))
        qubo[key] = qubo.get(key, 0) + value

    variables = [f"agents_{agents}" for agents in range(1, max_agents + 1)]

    for agents, variable in enumerate(variables, start=1):
        add(variable, variable, score_staffing_choice(agents, required))

    # One-hot constraint: penalty * (sum(x) - 1)^2
    for variable in variables:
        add(variable, variable, -penalty)

    for i in range(len(variables)):
        for j in range(i + 1, len(variables)):
            add(variables[i], variables[j], 2 * penalty)

    for variable in variables:
        add(variable, variable, penalty)

    return qubo


def build_staffing_plan(input_path, output_path="data/staffing_plan.csv"):
    df = pd.read_csv(input_path, parse_dates=["timestamp"])
    planned_agents = []
    required = []
    service_level_target = []

    for row in df.itertuples(index=False):
        needed = required_agents(row.forecast_calls, row.avg_handle_time_minutes)
        planned = solve_hour_classically(needed, max_agents=max(needed + 20, 30))

        required.append(needed)
        planned_agents.append(planned)
        service_level_target.append(0.80)

    df["required_agents"] = required
    df["planned_agents"] = planned_agents
    df["service_level_target"] = service_level_target
    df["staffing_gap"] = df["planned_agents"] - df["required_agents"]

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return df


if __name__ == "__main__":
    build_staffing_plan("data/forecast_output.csv")
