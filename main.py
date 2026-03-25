#!/usr/bin/env python3
"""
Main script to run the electricity peak analysis dashboard.
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install required packages."""
    print("Installing dependencies...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])

def generate_initial_data():
    """Generate initial meter data."""
    print("Generating initial meter data...")
    from data_generator import generate_meter_data
    dorms = ['Dorm A', 'Dorm B', 'Dorm C', 'Dorm D']
    df = generate_meter_data(dorms)
    df.to_csv('meter_data.csv', index=False)
    print("Data generated.")

def run_analysis():
    """Run data analysis."""
    print("Running analysis...")
    from analysis import analyze_data
    df, predictions = analyze_data()
    print("Analysis complete.")

def start_dashboard():
    """Start the Dash dashboard."""
    print("Starting dashboard...")
    from dashboard import app
    app.run(debug=True, host='0.0.0.0', port=8051)

if __name__ == "__main__":
    if not os.path.exists('meter_data.csv'):
        generate_initial_data()
        run_analysis()

    start_dashboard()