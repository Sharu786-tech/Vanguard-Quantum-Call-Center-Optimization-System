from pathlib import Path

import pandas as pd
import streamlit as st

try:
    import pandas as pd  # type: ignore[reportMissingImports]
except ImportError:
    st.error("Pandas is required to run this app. Install it with `pip install pandas`.")
    st.stop()

st.set_page_config(page_title="Vanguard Call Center Optimizer", layout="wide")
st.title("Vanguard Call Center Quantum Optimization")

results_path = Path("data/simulation_results.csv")

if not results_path.exists():
    st.warning("Run `python run_pipeline.py` first to generate dashboard data.")
    st.stop()

df = pd.read_csv(results_path, parse_dates=["timestamp"])

col1, col2, col3, col4 = st.columns(4)
col1.metric("Avg Forecast Calls", f"{df['forecast_calls'].mean():.0f}")
col2.metric("Avg Planned Agents", f"{df['planned_agents'].mean():.0f}")
col3.metric("Avg Service Level", f"{df['simulated_service_level'].mean():.1%}")
col4.metric("Target Hit Rate", f"{df['meets_target'].mean():.1%}")

st.subheader("Hourly Forecast and Staffing")
chart_df = df.set_index("timestamp")[["forecast_calls", "required_agents", "planned_agents"]]
st.line_chart(chart_df)

st.subheader("Service Level Simulation")
service_df = df.set_index("timestamp")[["simulated_service_level", "service_level_target"]]
st.line_chart(service_df)

st.subheader("Detailed Plan")
st.dataframe(
    df[
        [
            "timestamp",
            "forecast_calls",
            "required_agents",
            "planned_agents",
            "staffing_gap",
            "simulated_service_level",
            "simulated_avg_wait_seconds",
            "meets_target",
        ]
    ],
    use_container_width=True,
)
