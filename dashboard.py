import dash
from dash import html, dcc, Input, Output
import plotly.graph_objects as go
import pandas as pd
from analysis import analyze_data
from data_generator import generate_meter_data
import time

# Initialize app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Dorm Electricity Peak Hour Dashboard", style={'textAlign': 'center'}),

    dcc.Interval(
        id='interval-component',
        interval=60*1000,  # Update every minute
        n_intervals=0
    ),

    html.Div([
        html.Label("Select Dorm:"),
        dcc.Dropdown(
            id='dorm-dropdown',
            options=[{'label': dorm, 'value': dorm} for dorm in ['Dorm A', 'Dorm B', 'Dorm C', 'Dorm D']],
            value='Dorm A',
            style={'width': '50%'}
        )
    ], style={'padding': '20px'}),

    dcc.Graph(id='consumption-graph'),

    dcc.Graph(id='prediction-graph'),

    html.Div(id='peak-info', style={'padding': '20px', 'fontSize': '18px'})
])

@app.callback(
    [Output('consumption-graph', 'figure'),
     Output('prediction-graph', 'figure'),
     Output('peak-info', 'children')],
    [Input('interval-component', 'n_intervals'),
     Input('dorm-dropdown', 'value')]
)
def update_graphs(n, selected_dorm):
    # Regenerate data for live effect (in real scenario, fetch new data)
    dorms = ['Dorm A', 'Dorm B', 'Dorm C', 'Dorm D']
    df_raw = generate_meter_data(dorms, hours_back=168)
    df_raw.to_csv('meter_data.csv', index=False)

    # Analyze
    df, predictions = analyze_data()

    # Filter for selected dorm
    df_dorm = df[df['dorm'] == selected_dorm]
    pred_dorm = predictions[predictions['dorm'] == selected_dorm]

    # Consumption graph
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=df_dorm['timestamp'], y=df_dorm['consumption_kwh'],
                             mode='lines', name='Raw Consumption', line=dict(color='blue')))
    fig1.add_trace(go.Scatter(x=df_dorm['timestamp'], y=df_dorm['smoothed_consumption'],
                             mode='lines', name='Smoothed Consumption', line=dict(color='red')))
    fig1.update_layout(title=f'Hourly Consumption for {selected_dorm}',
                      xaxis_title='Time', yaxis_title='Consumption (kWh)')

    # Prediction graph
    fig2 = go.Figure()
    if not pred_dorm.empty:
        fig2.add_trace(go.Scatter(x=pred_dorm['timestamp'], y=pred_dorm['predicted_peak_kwh'],
                                 mode='lines+markers', name='Predicted Peaks', line=dict(color='orange')))
    fig2.update_layout(title=f'Predicted Evening Peaks for {selected_dorm}',
                      xaxis_title='Time', yaxis_title='Predicted Peak (kWh)')

    # Peak info
    if not pred_dorm.empty:
        max_pred = pred_dorm['predicted_peak_kwh'].max()
        peak_time = pred_dorm.loc[pred_dorm['predicted_peak_kwh'].idxmax(), 'timestamp']
        info = f"Predicted maximum peak: {max_pred} kWh at {peak_time.strftime('%Y-%m-%d %H:%M')}"
    else:
        info = "No predictions available"

    return fig1, fig2, info

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8051)