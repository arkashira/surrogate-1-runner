import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import requests
import dashboard_config as config
from typing import Dict

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1(config.DASHBOARD_TITLE),
    dcc.Tabs(id="tabs", value="recommendations", children=[
        dcc.Tab(label="Recommendations", value="recommendations"),
        dcc.Tab(label="Workflow", value="workflow"),
    ]),
    html.Div(id="tab-content"),
    dcc.Interval(
        id="recommendations-interval",
        interval=config.RECOMMENDATIONS_UPDATE_INTERVAL,
        n_intervals=0
    )
])

@app.callback(Output("tab-content", "children"), [Input("tabs", "value")])
def render_tab_content(tab):
    if tab == "recommendations":
        return html.Div([
            html.H3("AI-Powered Recommendations"),
            html.Div(id="recommendations-container"),
        ])
    elif tab == "workflow":
        return html.Div([
            html.H3("Workflow"),
            # Add workflow content here
        ])

@app.callback(
    Output("recommendations-container", "children"),
    [Input("recommendations-interval", "n_intervals")]
)
def update_recommendations(n):
    recommendations = fetch_recommendations()
    return [html.Div(recommendation["description"]) for recommendation in recommendations]

def fetch_recommendations() -> Dict:
    response = requests.get(config.RECOMMENDATIONS_API_ENDPOINT)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    app.run_server(debug=True)