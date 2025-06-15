import dash
import pandas as pd
from dash import Dash, dash_table, dcc, html, Input, Output, State
import plotly.express as px
from map import get_viz2


app = Dash(__name__)
server = app.server
# Persistent state for each visualization
app.layout = html.Div([
    html.H2("Project Team 14", style={"marginBottom": 20}),
    # Persistent navigation bar, centered
    html.Div(
        [
            dcc.Tabs(
                id="tabs",
                value="viz1",
                children=[
                    dcc.Tab(label="Visualization 1", value="viz1"),
                    dcc.Tab(label="Visualization 2", value="viz2"),
                    dcc.Tab(label="Visualization 3", value="viz3"),
                    dcc.Tab(label="Visualization 4", value="viz4"),
                    dcc.Tab(label="Visualization 5", value="viz5"),
                ],
                style={"width": "60vw", "margin": "0 auto"},
            )
        ],
        style={
            "position": "fixed",
            "top": "50%",
            "left": "50%",
            "transform": "translate(-50%, -50%)",
            "zIndex": 1000,
            "background": "#fff",
            "boxShadow": "0 2px 8px rgba(0,0,0,0.1)",
            "borderRadius": "8px",
            "padding": "10px"
        }
    ),
    # Hidden stores for state preservation
    dcc.Store(id="store-viz1"),
    dcc.Store(id="store-viz2"),
    dcc.Store(id="store-viz3"),
    dcc.Store(id="store-viz4"),
    dcc.Store(id="store-viz5"),
    # Main content area
    html.Div(id="tab-content", style={"marginTop": "200px"})
])

# Callback to render the selected tab's content
@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "value"),
    State("store-viz1", "data"),
    State("store-viz2", "data"),
    State("store-viz3", "data"),
    State("store-viz4", "data"),
    State("store-viz5", "data"),
)
def render_content(tab, s1, s2, s3, s4, s5):
    if tab == "viz1":
        return html.Div("Visualization 1 goes here")
    elif tab == "viz2":
         return html.Div([
        html.H4("Carte des crimes à Montréal"),
        get_viz2()
    ])
    elif tab == "viz3":
        return html.Div("Visualization 3 goes here")
    elif tab == "viz4":
        return html.Div("Visualization 4 goes here")
    elif tab == "viz5":
        return html.Div("Visualization 5 goes here")
    return html.Div("Select a visualization.")

if __name__ == "__main__":
    app.run(debug=True)