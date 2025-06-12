import html
from dash import Input, Output
import visualizations.viz1 as viz1

def register_callbacks(app):

    @app.callback(
        Output("viz1-graph", "figure"),
        Input("viz1-view-dropdown", "value"),
        Input("viz1-chart-type", "value")
    )
    def update_viz1_graph(view, chart_type):
        return viz1.update_graph(view, chart_type)


    # Callback to render the selected tab's content
    @app.callback(
        Output("tab-content", "children"),
        Input("tabs", "value")
    )
    def render_tab(tab):
        if tab == "viz1":
            return viz1.layout()
        # elif tab == "viz2":
        #     return html.Div("Visualization 2 goes here")
        # elif tab == "viz3":
        #     return html.Div("Visualization 3 goes here")
        # elif tab == "viz4":
        #     return html.Div("Visualization 4 goes here")
        # elif tab == "viz5":
        #     return html.Div("Visualization 5 goes here")
        return html.Div("Select a visualization.")