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

time_translation = {
    "Jour": "Day",
    "Soir": "Evening",
    "Nuit": "Night"
}

crime_translation = {
    "Vol De Véhicule À Moteur": "Motor Vehicle Theft",
    "Méfait": "Mischief",
    "Vol Dans / Sur Véhicule À Moteur": "Theft From/In Motor Vehicle",
    "Introduction": "Breaking And Entering",
    "Vols Qualifiés": "Robbery",
    "Infractions Entrainant La Mort": "Offences Causing Death"
}

df["QUART"] = df["QUART"].str.strip().str.capitalize().map(time_translation)
df["CrimeType"] = df["CrimeType"].map(crime_translation).fillna(df["CrimeType"])

heat_time = df.groupby(["CrimeType", "QUART"]).size().unstack(fill_value=0)
heat_season = df.groupby(["CrimeType", "Season"]).size().unstack(fill_value=0)
heat_year = df.groupby(["CrimeType", "Year"]).size().unstack(fill_value=0)

def layout():
    fig = go.Figure()

    fig.add_trace(go.Heatmap(
        z=heat_time.values,
        x=heat_time.columns,
        y=heat_time.index,
        colorscale="YlOrRd",
        colorbar_title="Number of Crimes",
        visible=True,
        name="Time of Day",
        hovertemplate="<b>Crime Type:</b> %{y}<br><b>Time:</b> %{x}<br><b>Count:</b> %{z}<extra></extra>"
    ))

    fig.add_trace(go.Heatmap(
        z=heat_season.values,
        x=heat_season.columns,
        y=heat_season.index,
        colorscale="YlOrRd",
        colorbar_title="Number of Crimes",
        visible=False,
        name="Season",
        hovertemplate="<b>Crime Type:</b> %{y}<br><b>Season:</b> %{x}<br><b>Count:</b> %{z}<extra></extra>"
    ))

    fig.add_trace(go.Heatmap(
        z=heat_year.values,
        x=heat_year.columns.astype(str),
        y=heat_year.index,
        colorscale="YlOrRd",
        colorbar_title="Number of Crimes",
        visible=False,
        name="Year",
        hovertemplate="<b>Crime Type:</b> %{y}<br><b>Year:</b> %{x}<br><b>Count:</b> %{z}<extra></extra>"
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