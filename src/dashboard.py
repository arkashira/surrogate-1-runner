import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define layout
layout = dbc.Container(
    [
        html.H1("Shell Access Dashboard"),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button("Launch Shell Session", color="primary", id="launch-button"),
                    md=4,
                ),
                dbc.Col(
                    dbc.Select(
                        id="instance-select",
                        options=[
                            {"label": "Instance 1", "value": "instance-1"},
                            {"label": "Instance 2", "value": "instance-2"},
                        ],
                    ),
                    md=4,
                ),
            ],
            justify="around",
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(id="session-status"),
                    md=4,
                ),
            ],
            justify="around",
        ),
    ],
    className="p-5",
)

# Define callback for launching shell session
@app.callback(
    Output("session-status", "children"),
    [Input("launch-button", "n_clicks")],
    [dash.dependencies.State("instance-select", "value")],
)
def launch_session(n_clicks, instance_value):
    if n_clicks is not None and instance_value is not None:
        # Launch shell session logic goes here
        return f"Launched shell session on {instance_value}"
    return "No session launched"

# Run app
if __name__ == "__main__":
    app.run_server(debug=True)