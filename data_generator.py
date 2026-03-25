import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_meter_data(dorms, hours_back=168):  # 168 hours = 1 week
    """
    Generate synthetic hourly electricity meter data for dorms.
    Includes patterns: higher consumption in evenings, weekends, etc.
    """
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=hours_back)

    # Create hourly datetime index
    datetime_index = pd.date_range(start=start_time, end=end_time, freq='h')

    data = []

    for dorm in dorms:
        np.random.seed(hash(dorm) % 2**32)  # Reproducible seed per dorm

        base_consumption = np.random.uniform(50, 100)  # kWh base

        for dt in datetime_index:
            hour = dt.hour
            weekday = dt.weekday() < 5  # True for Mon-Fri

            # Base consumption
            consumption = base_consumption

            # Evening peak (6-10 PM)
            if 18 <= hour <= 22:
                consumption *= np.random.uniform(1.5, 2.5)

            # Morning peak (7-9 AM on weekdays)
            elif weekday and 7 <= hour <= 9:
                consumption *= np.random.uniform(1.2, 1.8)

            # Weekend higher consumption
            if not weekday:
                consumption *= np.random.uniform(1.1, 1.3)

            # Add noise
            consumption *= np.random.uniform(0.8, 1.2)

            data.append({
                'timestamp': dt,
                'dorm': dorm,
                'consumption_kwh': round(consumption, 2)
            })

    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    dorms = ['Dorm A', 'Dorm B', 'Dorm C', 'Dorm D']
    df = generate_meter_data(dorms)
    df.to_csv('meter_data.csv', index=False)
    print("Generated meter data saved to meter_data.csv")