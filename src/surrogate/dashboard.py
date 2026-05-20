import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Contract Change Dashboard'),
    dcc.Interval(
        id='interval-component',
        interval=1*1000, # in milliseconds
        n_intervals=0
    ),
    html.Div(id='output-container')
])

@app.callback(
    Output('output-container', 'children'),
    [Input('interval-component', 'n_intervals')]
)
def update_output(n):
    # TO DO: implement logic to detect changes in request signature
    # and surface them in real-time alerts and a central dashboard
    return 'No changes detected'

if __name__ == '__main__':
    app.run_server(debug=True)