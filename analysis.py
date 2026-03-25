import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

def load_data(filepath='meter_data.csv'):
    df = pd.read_csv(filepath, parse_dates=['timestamp'])
    df = df.sort_values(['dorm', 'timestamp'])
    return df

def apply_moving_average(df, window=3):
    """
    Apply moving average smoothing to consumption data.
    """
    df['smoothed_consumption'] = df.groupby('dorm')['consumption_kwh'].transform(
        lambda x: x.rolling(window=window, center=True).mean()
    )
    # Fill NaN values at edges
    df['smoothed_consumption'] = df['smoothed_consumption'].bfill().ffill()
    return df

def predict_evening_peaks(df):
    """
    Use linear regression to predict evening peaks (6-10 PM) based on past week.
    """
    predictions = []

    for dorm in df['dorm'].unique():
        dorm_data = df[df['dorm'] == dorm].copy()

        # Focus on evening hours (18-22)
        evening_data = dorm_data[(dorm_data['timestamp'].dt.hour >= 18) & (dorm_data['timestamp'].dt.hour <= 22)]

        if len(evening_data) < 10:  # Need minimum data
            continue

        # Features: hour, day of week, day of month
        evening_data['hour'] = evening_data['timestamp'].dt.hour
        evening_data['day_of_week'] = evening_data['timestamp'].dt.dayofweek
        evening_data['day_of_month'] = evening_data['timestamp'].dt.day

        # Target: consumption
        X = evening_data[['hour', 'day_of_week', 'day_of_month']]
        y = evening_data['consumption_kwh']

        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Train model
        model = LinearRegression()
        model.fit(X_scaled, y)

        # Predict for next few days
        future_dates = pd.date_range(start=df['timestamp'].max() + pd.Timedelta(hours=1),
                                   periods=24, freq='h')  # Next 24 hours

        future_evening = future_dates[(future_dates.hour >= 18) & (future_dates.hour <= 22)]

        future_X = pd.DataFrame({
            'hour': future_evening.hour,
            'day_of_week': future_evening.dayofweek,
            'day_of_month': future_evening.day
        })

        future_X_scaled = scaler.transform(future_X)
        predicted_consumption = model.predict(future_X_scaled)

        for dt, pred in zip(future_evening, predicted_consumption):
            predictions.append({
                'timestamp': dt,
                'dorm': dorm,
                'predicted_peak_kwh': max(0, round(pred, 2))  # Ensure non-negative
            })

    pred_df = pd.DataFrame(predictions)
    return pred_df

def analyze_data():
    df = load_data()
    df = apply_moving_average(df)
    predictions = predict_evening_peaks(df)
    return df, predictions

if __name__ == "__main__":
    df, predictions = analyze_data()
    print("Data analysis complete.")
    print(f"Total records: {len(df)}")
    print(f"Predictions: {len(predictions)}")
    predictions.to_csv('predictions.csv', index=False)
    print("Predictions saved to predictions.csv")