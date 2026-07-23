from pathlib import Path

import numpy as np
import pandas as pd


def generate_sample_data(output_path="data/call_center_sample.csv", days=60, seed=42):
    rng = np.random.default_rng(seed)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    start = pd.Timestamp("2026-01-01 08:00:00")
    rows = []

    for day in range(days):
        current_day = start + pd.Timedelta(days=day)
        weekday = current_day.weekday()
        market_event = int(rng.random() < 0.12)

        for hour in range(8, 20):
            hour_factor = 1.0 + 0.45 * np.exp(-((hour - 10) ** 2) / 8)
            afternoon_factor = 1.0 + 0.30 * np.exp(-((hour - 15) ** 2) / 10)
            weekday_factor = 1.2 if weekday < 5 else 0.55
            event_factor = 1.35 if market_event else 1.0

            expected_calls = 80 * hour_factor * afternoon_factor * weekday_factor * event_factor
            call_volume = max(0, int(rng.normal(expected_calls, expected_calls * 0.12)))
            avg_handle_time_minutes = max(4.5, rng.normal(8.0, 1.0))

            rows.append(
                {
                    "timestamp": current_day.replace(hour=hour),
                    "weekday": weekday,
                    "hour": hour,
                    "market_event": market_event,
                    "call_volume": call_volume,
                    "avg_handle_time_minutes": round(avg_handle_time_minutes, 2),
                }
            )

    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
    return df


if __name__ == "__main__":
    generate_sample_data()
