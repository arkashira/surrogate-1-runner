import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import yaml

class ComplianceDashboard:
    def __init__(self):
        self.config = self.load_config()

    def load_config(self):
        with open('/opt/axentx/surrogate-1/src/config/compliance_config.yaml', 'r') as f:
            return yaml.safe_load(f)

    def render(self):
        return html.Div([
            html.H1('Compliance Settings'),
            html.Div([
                html.Label('Setting 1:'),
                dcc.Input(id='setting-1', type='text'),
                html.Div(id='setting-1-output')
            ]),
            html.Div([
                html.Label('Setting 2:'),
                dcc.Input(id='setting-2', type='text'),
                html.Div(id='setting-2-output')
            ])
        ])

    @dash.dependencies.Input('setting-1', 'value')
    def update_setting_1_output(self, value):
        return html.Div(f'Setting 1: {value}')

    @dash.dependencies.Input('setting-2', 'value')
    def update_setting_2_output(self, value):
        return html.Div(f'Setting 2: {value}')

app = dash.Dash(__name__)
app.layout = ComplianceDashboard().render()
if __name__ == '__main__':
    app.run_server(debug=True)