# Peak Hour Electricity Spikes Analysis

This project collects hourly electricity meter data from dormitories, applies moving average smoothing, uses linear regression to predict evening peaks based on the past week's data, and visualizes trends on a live Plotly dashboard.

## Features

- **Data Collection**: Simulates hourly meter data from multiple dorms with realistic consumption patterns
- **Data Smoothing**: Applies moving average smoothing to reduce noise
- **Peak Prediction**: Uses linear regression to forecast evening electricity peaks
- **Live Dashboard**: Interactive Plotly dashboard with real-time updates

## Installation

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the main script to start the dashboard:

```bash
python main.py
```

The dashboard will be available at http://localhost:8051

## Project Structure

- `main.py`: Main entry point
- `data_generator.py`: Generates synthetic meter data
- `analysis.py`: Performs smoothing and prediction analysis
- `dashboard.py`: Dash application for visualization
- `requirements.txt`: Python dependencies
- `meter_data.csv`: Generated meter data
- `predictions.csv`: Prediction results

## Data

The system generates synthetic hourly consumption data for 4 dorms over the past week, including:
- Base consumption patterns
- Evening peaks (6-10 PM)
- Morning peaks on weekdays
- Weekend variations
- Random noise

## Analysis

- **Moving Average**: 3-hour centered moving average for smoothing
- **Linear Regression**: Predicts evening peaks using hour, day of week, and day of month as features