import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from performance_metrics import PerformanceMetrics
from gpu_scaler import GPUScaler

app = dash.Dash(__name__)

performance_metrics = PerformanceMetrics()
gpu_scaler = GPUScaler(target_fps=60, performance_metrics=performance_metrics)

app.layout = html.Div([
    html.H1("Performance Metrics Dashboard"),
    dcc.Graph(id='gpu-metrics'),
    dcc.Graph(id='cpu-metrics'),
    dcc.Graph(id='memory-metrics'),
    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # in milliseconds
        n_intervals=0
    )
])

@app.callback(
    [Output('gpu-metrics', 'figure'),
     Output('cpu-metrics', 'figure'),
     Output('memory-metrics', 'figure')],
    [Input('interval-component', 'n_intervals')]
)
def update_metrics(n):
    metrics = performance_metrics.get_all_metrics()
    gpu_scaler.scale_gpu()

    gpu_fig = go.Figure()
    for gpu_id, gpu_data in metrics['gpu'].items():
        gpu_fig.add_trace(go.Scatter(
            x=[gpu_id],
            y=[gpu_data['load']],
            mode='markers',
            name=f'GPU {gpu_id} Load'
        ))

    cpu_fig = go.Figure()
    cpu_fig.add_trace(go.Scatter(
        x=['CPU'],
        y=[metrics['cpu']['cpu_percent']],
        mode='markers',
        name='CPU Usage'
    ))

    memory_fig = go.Figure()
    memory_fig.add_trace(go.Scatter(
        x=['Memory'],
        y=[metrics['memory']['memory_percent']],
        mode='markers',
        name='Memory Usage'
    ))

    return gpu_fig, cpu_fig, memory_fig

if __name__ == '__main__':
    app.run_server(debug=True)