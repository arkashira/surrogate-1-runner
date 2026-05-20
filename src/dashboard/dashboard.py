import dash
from dash import dcc, html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Guide Resolution Dashboard'),
    dcc.Graph(id='resolution-graph'),
    dcc.Interval(
        id='interval-component',
        interval=1*60*60*24*7, # 1 week in milliseconds
        n_intervals=0
    )
])

@app.callback(
    Output('resolution-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    # TO DO: fetch data from database or logs
    return {
        'data': [
            {'x': [1, 2, 3], 'y': [10, 20, 30]}
        ],
        'layout': {
            'title': 'Guide Resolution Metrics'
        }
    }

if __name__ == '__main__':
    app.run_server(debug=True)