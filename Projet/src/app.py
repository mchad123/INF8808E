from dash import Dash, dcc, html
from visualizations import viz1, viz2
from callbacks import register_callbacks

app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server

app.layout = html.Div([
    # Top navigation bar with tabs
    html.Div(
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
        ),
        style={
            "position": "fixed",
            "top": "0",
            "left": "50%",
            "transform": "translateX(-50%)",
            "width": "80vw",
            "background": "#fff",
            "zIndex": 1000,
            "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
            "borderRadius": "0 0 8px 8px",
            "padding": "10px"
        }
    ),
    # Stores (hidden, used for data/state)
    html.Div([
        dcc.Store(id="store-viz1"),
        dcc.Store(id="store-viz2"),
        dcc.Store(id="store-viz3"),
        dcc.Store(id="store-viz4"),
        dcc.Store(id="store-viz5"),
    ]),
    # Main content area (pushed down to avoid overlap with fixed top bar)
    html.Div([
        html.H2("Project Team 14", style={"marginBottom": "20px"}),
        html.Div(id="tab-content")  # Dynamically injected tab content
    ], style={"marginTop": "120px", "padding": "20px"})
])

register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)