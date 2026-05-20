import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

# Mock data for demonstration purposes
data = {
    'Component': ['CPU', 'GPU', 'RAM', 'Storage'],
    'Current Rig Performance': [100, 200, 300, 400],
    'Proposed Upgrade Performance': [150, 250, 350, 450],
    'Game': ['Game A', 'Game B', 'Game C', 'Game D']
}

df = pd.DataFrame(data)

app.layout = html.Div([
    html.H1("Gaming Rig Performance Comparison"),
    dcc.Dropdown(
        id='component-dropdown',
        options=[{'label': i, 'value': i} for i in df['Component'].unique()],
        value='CPU'
    ),
    dcc.Dropdown(
        id='game-dropdown',
        options=[{'label': i, 'value': i} for i in df['Game'].unique()],
        value='Game A'
    ),
    dcc.Graph(id='performance-graph')
])

@app.callback(
    Output('performance-graph', 'figure'),
    [Input('component-dropdown', 'value'), Input('game-dropdown', 'value')]
)
def update_graph(selected_component, selected_game):
    filtered_df = df[(df['Component'] == selected_component) & (df['Game'] == selected_game)]
    fig = px.bar(filtered_df, x=['Current Rig Performance', 'Proposed Upgrade Performance'], y='Component', title=f'Performance Comparison for {selected_game}')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)