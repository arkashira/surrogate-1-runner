import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Alert Dashboard'),
    html.Div(children='''
        This dashboard displays real-time alerts for potential errors or discrepancies.
    '''),
    dcc.Graph(id='alert-graph'),
    dcc.Interval(
        id='interval-component',
        interval=60000, # in milliseconds
        n_intervals=0
    )
])

@app.callback(
    Output('alert-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    # Fetch latest alert data
    alerts = pd.read_csv('alerts.csv')
    
    # Create figure
    fig = px.bar(alerts, x='alert_type', y='count')
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)