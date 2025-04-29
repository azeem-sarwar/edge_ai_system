# Content of prophet_analysis.py
from prophet import Prophet
import pandas as pd

def check_anomaly(sensor_data):
    df = pd.DataFrame(sensor_data)
    df.rename(columns={'timestamp': 'ds', 'value': 'y'}, inplace=True)

    model = Prophet()
    model.fit(df)

    future = model.make_future_dataframe(periods=3, freq='min')
    forecast = model.predict(future)

    anomalies = []
    for actual, predicted in zip(df['y'], forecast['yhat'][:len(df)]):
        if abs(actual - predicted) > 0.2 * predicted:
            anomalies.append({"value": actual, "predicted": predicted})

    return anomalies
# This function checks for anomalies in the sensor data using the Prophet model.
# It returns a list of anomalies detected.
# The function takes a list of sensor data as input, which should be in the format:
# [{'timestamp': '2023-10-01T12:00:00Z', 'value': 25.0}, ...]
# The function uses the Prophet library to fit a model to the data and predict future values.