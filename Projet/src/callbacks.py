from dash import Input, Output, html
import visualizations.viz1 as viz1
import visualizations.viz2 as viz2
import visualizations.viz3 as viz3
import visualizations.viz4 as viz4
import visualizations.viz5 as viz5

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
        elif tab == "viz2":
            return viz2.layout()
        elif tab == "viz3":
           return viz3.layout()
        elif tab == "viz4":
            return viz4.layout()
        elif tab == "viz5":
            return viz5.layout()
        return html.Div("Select a visualization.")

    @app.callback(
        Output("bar-chart", "figure"),
        Output("pie-chart", "figure"),
        Output("line-chart", "figure"),
        Input("pdq-dropdown", "value"),
        Input("year-slider", "value")
    )
    def update_all_charts(selected_pdq, selected_years):
        start_year, end_year = selected_years
        pdq_value = None if selected_pdq == "All" else selected_pdq

        filtered_df = viz2.filter_data(start_year, end_year, pdq=pdq_value)

        bar_fig = viz2.create_bar_chart(filtered_df)
        pie_fig = viz2.create_pie_chart(filtered_df)
        line_fig = viz2.create_line_chart(filtered_df)

        return bar_fig, pie_fig, line_fig