import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import time
from datetime import datetime, timedelta

app = dash.Dash(__name__)

# Initialize the app layout
app.layout = html.Div([
    html.H1("Real-Time Cost Dashboard"),
    dcc.Dropdown(
        id='service-filter',
        options=[
            {'label': 'All Services', 'value': 'all'},
            {'label': 'Compute', 'value': 'compute'},
            {'label': 'Storage', 'value': 'storage'},
            {'label': 'Network', 'value': 'network'}
        ],
        value='all'
    ),
    dcc.DatePickerRange(
        id='date-range',
        start_date=datetime.today() - timedelta(days=7),
        end_date=datetime.today()
    ),
    dcc.Graph(id='cost-graph'),
    dcc.Interval(
        id='interval-component',
        interval=300000,  # 5 minutes in milliseconds
        n_intervals=0
    )
])

# Callback to update the graph
@app.callback(
    Output('cost-graph', 'figure'),
    [Input('interval-component', 'n_intervals'),
     Input('service-filter', 'value'),
     Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_graph(n, service, start_date, end_date):
    # Simulate fetching real-time cost data
    # In a real application, this would be replaced with an API call to your cost data service
    data = {
        'timestamp': [datetime.now() - timedelta(minutes=i) for i in range(60)],
        'cost': [100 + i * 5 + (i % 10) * 20 for i in range(60)],
        'service': ['compute' if i % 3 == 0 else 'storage' if i % 3 == 1 else 'network' for i in range(60)]
    }
    df = pd.DataFrame(data)

    # Filter data based on user inputs
    df = df[df['timestamp'] >= pd.to_datetime(start_date)]
    df = df[df['timestamp'] <= pd.to_datetime(end_date)]
    if service != 'all':
        df = df[df['service'] == service]

    # Create the figure
    fig = px.line(df, x='timestamp', y='cost', color='service', title='Real-Time Cost Data')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)