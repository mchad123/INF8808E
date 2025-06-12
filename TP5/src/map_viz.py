'''
    Contains the functions to set up the map visualization.

'''

import plotly.graph_objects as go
import plotly.express as px

import hover_template as hover

COLOR_MAP = {
    'Noyau villageois': '#626ff5',
    'Passage entre rues résidentielles': '#E74C3C',
    'Rue bordant un bâtiment public ou institutionnel': '#1ABC9C',
    'Rue commerciale de quartier, d’ambiance ou de destination': '#9B59B6',
    'Rue en bordure ou entre deux parcs ou place publique': '#F39C12',
    'Rue entre un parc et un bâtiment public ou institutionnel': '#00BCD4',
    'Rue transversale à une rue commerciale': '#F06292'
}

def add_choro_trace(fig, montreal_data, locations, z_vals, colorscale):
    '''
        Adds the choropleth trace, representing Montreal's neighborhoods.

        Note: The z values and colorscale provided ensure every neighborhood
        will be grey in color. Although the trace is defined using Plotly's
        choropleth features, we are simply defining our base map.

        The opacity of the map background color should be 0.2.

        Args:
            fig: The figure to add the choropleth trace to
            montreal_data: The data used for the trace
            locations: The locations (neighborhoods) to show on the trace
            z_vals: The table to use for the choropleth's z values
            colorscale: The table to use for the choropleth's color scale
        Returns:
            fig: The updated figure with the choropleth trace

    '''
    # TODO : Draw the map base
    fig.add_choroplethmapbox(
        geojson=montreal_data,
        locations=locations,
        z=z_vals,
        featureidkey='properties.NOM',
        colorscale=colorscale,
        showscale=False,
        marker_opacity=0.2,
        hovertemplate=hover.map_base_hover_template()
    )
    return fig

def add_scatter_traces(fig, street_df):
    '''
        Adds the scatter trace, representing Montreal's pedestrian paths.

        The marker size should be 20.

        Args:
            fig: The figure to add the scatter trace to
            street_df: The dataframe containing the information on the
                pedestrian paths to display
        Returns:
            The figure now containing the scatter trace

    '''
    # TODO : Add the scatter markers to the map base
    types = street_df["TYPE_SITE_INTERVENTION"].unique()

    for site_type in types:
        df_type = street_df[street_df["TYPE_SITE_INTERVENTION"] == site_type]
        latitudes = df_type["geometry"].apply(lambda g: g["coordinates"][1])
        longitudes = df_type["geometry"].apply(lambda g: g["coordinates"][0])

        customdata = []
        for _, row in df_type.iterrows():
            custom_row = [
                row.get('NOM_PROJET', ''),
                row.get('MODE_IMPLANTATION', ''),
                row.get('OBJECTIF_THEMATIQUE', '')
            ]
            customdata.append(custom_row)

        fig.add_trace(go.Scattermapbox(
            lat=latitudes,
            lon=longitudes,
            mode='markers',
            marker=dict(
                size=20,
                color=COLOR_MAP.get(site_type, "#000000")
            ),
            name=site_type,
            hovertemplate=hover.map_marker_hover_template(site_type),
            customdata=customdata
        ))

    return fig