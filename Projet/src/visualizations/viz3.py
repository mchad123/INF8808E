from dash import html, dcc
import pandas as pd
import geopandas as gpd
import plotly.graph_objects as go
import json
from shapely.geometry import Point

def crime_hover_template(crime_type):
    return (
        f"<b>{crime_type}</b><br>" +
        "Quartier: %{customdata[1]}<br>" +
        "PDQ: %{customdata[0]}<extra></extra>"
    )

def base_hover_template():
    return "Quartier: %{location}<extra></extra>"


with open("data/montreal.json") as f:
    montreal_geo = json.load(f)

gdf_quartiers = gpd.read_file("data/montreal.json")
df = pd.read_csv("data/actes-criminels.csv")

df.rename(columns={
    "CATEGORIE": "CrimeType",
    "LONGITUDE": "Longitude",
    "LATITUDE": "Latitude",
    "PDQ": "PDQ"
}, inplace=True)

df = df.dropna(subset=["Longitude", "Latitude"]).copy()
df["CrimeType"] = df["CrimeType"].str.strip().str.lower().str.title()
df["PDQ"] = df["PDQ"].astype(str)

df = df[(df["Latitude"] > 45.40) & (df["Latitude"] < 45.70) &
        (df["Longitude"] > -73.95) & (df["Longitude"] < -73.45)]

df["geometry"] = df.apply(lambda row: Point(row["Longitude"], row["Latitude"]), axis=1)
gdf_crimes = gpd.GeoDataFrame(df, geometry="geometry", crs=gdf_quartiers.crs)


gdf_joined = gpd.sjoin(gdf_crimes, gdf_quartiers, how="left", predicate="within")
gdf_joined["Quartier"] = gdf_joined["NOM"] 

COLOR_MAP = {
    "Vol De Véhicule À Moteur": "#626ff5",
    "Méfait": "#E74C3C",
    "Vol Dans / Sur Véhicule À Moteur": "#1ABC9C",
    "Introduction": "#9B59B6",
    "Vols Qualifiés": "#F39C12",
    "Infractions Entrainant La Mort": "#00BCD4"
}

def layout():
    fig = go.Figure()

    neighborhoods = [feature["properties"]["NOM"] for feature in montreal_geo["features"]]
    z_vals = [1] * len(neighborhoods)

    fig.add_choroplethmapbox(
        geojson=montreal_geo,
        locations=neighborhoods,
        z=z_vals,
        featureidkey="properties.NOM",
        colorscale=[[0, "lightgrey"], [1, "lightgrey"]],
        showscale=False,
        marker_opacity=0.2,
        marker_line=dict(width=1.5, color="black"),
        hovertemplate=base_hover_template()
    )

    for crime_type, color in COLOR_MAP.items():
        gdf_type = gdf_joined[gdf_joined["CrimeType"] == crime_type].copy()

        fig.add_trace(go.Scattermapbox(
            lat=gdf_type["Latitude"],
            lon=gdf_type["Longitude"],
            mode="markers",
            marker=dict(size=6, color=color, opacity=0.7),
            name=crime_type,
            customdata=gdf_type[["PDQ", "Quartier"]],
            hovertemplate=crime_hover_template(crime_type)
        ))

    fig.update_layout(
        mapbox_style="white-bg",
        mapbox_zoom=10.5,
        mapbox_center={"lat": 45.55, "lon": -73.6},
        mapbox_bounds={"west": -73.95, "east": -73.45, "south": 45.40, "north": 45.70},
        height=750,
        margin=dict(t=20, r=0, l=0, b=0),
        legend_title="Type de crime"
    )

    return html.Div([
        html.H3("Explorez les crimes à Montréal"),
        dcc.Graph(figure=fig)
    ])
