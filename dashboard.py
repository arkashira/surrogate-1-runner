import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from metrics import get_performance_metrics

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Surrogate-1 Performance Monitoring Dashboard'),
    dcc.Graph(id='performance-metrics-graph'),
    dcc.Interval(
        id='interval-component',
        interval=1000, # in milliseconds
        n_intervals=0
    )
])

@app.callback(
    Output('performance-metrics-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    metrics = get_performance_metrics()
    df = pd.DataFrame(metrics)
    fig = px.line(df, x='time', y='metric')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)