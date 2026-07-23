from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split


FEATURES = ["weekday", "hour", "market_event", "avg_handle_time_minutes"]


def forecast_call_volume(input_path, output_path="data/forecast_output.csv"):
    df = pd.read_csv(input_path, parse_dates=["timestamp"])
    x = df[FEATURES]
    y = df["call_volume"]

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=7, shuffle=False
    )

    model = RandomForestRegressor(
        n_estimators=150,
        max_depth=8,
        random_state=7,
        min_samples_leaf=3,
    )
    model.fit(x_train, y_train)

    df["forecast_calls"] = model.predict(x).round().astype(int)
    mae = mean_absolute_error(y_test, model.predict(x_test))
    df["forecast_mae"] = round(mae, 2)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return df


if __name__ == "__main__":
    forecast_call_volume("data/call_center_sample.csv")
