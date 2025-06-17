import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc


df = pd.read_csv("data/actes-criminels.csv")
df.rename(columns={
    "CATEGORIE": "CrimeType",
    "LONGITUDE": "Longitude",
    "LATITUDE": "Latitude"
}, inplace=True)
df["DATE"] = pd.to_datetime(df["DATE"], errors="coerce")
df = df.dropna(subset=["DATE"])
df["Month"] = df["DATE"].dt.month
df["Year"] = df["DATE"].dt.year

def get_season(m):
    return (
        "Winter" if m in [12, 1, 2] else
        "Spring" if m in [3, 4, 5] else
        "Summer" if m in [6, 7, 8] else
        "Fall"
    )

df["Season"] = df["Month"].apply(get_season)
df["CrimeType"] = df["CrimeType"].str.strip().str.lower().str.title()

quart_translation = {
    "Jour": "Day",
    "Soir": "Evening",
    "Nuit": "Night"
}
df["QUART"] = df["QUART"].str.strip().str.capitalize().map(quart_translation)


heat_quart = df.groupby(["CrimeType", "QUART"]).size().unstack(fill_value=0)
heat_season = df.groupby(["CrimeType", "Season"]).size().unstack(fill_value=0)
heat_year = df.groupby(["CrimeType", "Year"]).size().unstack(fill_value=0)


def layout():
    fig = go.Figure()

    fig.add_trace(go.Heatmap(
        z=heat_quart.values,
        x=heat_quart.columns,
        y=heat_quart.index,
        colorscale="YlOrRd",
        colorbar_title="Crimes",
        visible=True,
        name="Time of Day"
    ))

    fig.add_trace(go.Heatmap(
        z=heat_season.values,
        x=heat_season.columns,
        y=heat_season.index,
        colorscale="YlOrRd",
        colorbar_title="Crimes",
        visible=False,
        name="Season",
        hovertemplate="<b>x:</b> %{x}<br><b>y:</b> %{y}<br><b>z:</b> %{z:.3s}<extra></extra>"
    ))

    fig.add_trace(go.Heatmap(
        z=heat_year.values,
        x=heat_year.columns.astype(str),
        y=heat_year.index,
        colorscale="YlOrRd",
        colorbar_title="Crimes",
        visible=False,
        name="Year",
        hovertemplate="<b>x:</b> %{x}<br><b>y:</b> %{y}<br><b>z:</b> %{z:.3s}<extra></extra>"
    ))

    fig.update_layout(
        updatemenus=[
            {
                "buttons": [
                    {"label": "By Time of Day", "method": "update", "args": [{"visible": [True, False, False]}, {"title": "Crime Types by Time of Day"}]},
                    {"label": "By Season", "method": "update", "args": [{"visible": [False, True, False]}, {"title": "Crime Types by Season"}]},
                    {"label": "By Year", "method": "update", "args": [{"visible": [False, False, True]}, {"title": "Crime Types by Year"}]}
                ],
                "direction": "down",
                "showactive": True,
                "x": 0.5,
                "xanchor": "center",
                "y": 1.1,
                "yanchor": "top"
            }
        ],
        title="Crime Heatmap Toggle View",
        height=800,
        margin=dict(t=100)
    )

    return html.Div([
        html.H3("Crime Heatmap Visualization"),
        dcc.Graph(figure=fig)
    ])