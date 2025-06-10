'''
    This file contains the functions to call when
    a click is detected on the map, depending on the context
'''
import dash_html_components as html
import re



def no_clicks(style):
    '''
        Deals with the case where the map was not clicked

        Args:
            style: The current display style for the panel
        Returns:
            title: The updated display title
            mode: The updated display title
            theme: The updated display theme
            style: The updated display style for the panel
    '''
    # TODO : Handle no clicks on the map
    return None, None, None, style


def map_base_clicked(title, mode, theme, style):
    '''
        Deals with the case where the map base is
        clicked (but not a marker)

        Args:
            title: The current display title
            mode: The current display title
            theme: The current display theme
            style: The current display style for the panel
        Returns:
            title: The updated display title
            mode: The updated display title
            theme: The updated display theme
            style: The updated display style for the panel
    '''
    # TODO : Handle clicks on the map base
    new_style = style.copy()
    new_style["display"] = "none"
    return title, mode, theme, style


def map_marker_clicked(figure, curve, point, title, mode, theme, style): # noqa : E501 pylint: disable=unused-argument too-many-arguments line-too-long
    '''
        Deals with the case where a marker is clicked

        Args:
            figure: The current figure
            curve: The index of the curve containing the clicked marker
            point: The index of the clicked marker
            title: The current display title
            mode: The current display title
            theme: The current display theme
            style: The current display style for the panel
        Returns:
            title: The updated display title
            mode: The updated display title
            theme: The updated display theme
            style: The updated display style for the panel
    '''
    # TODO : Handle clicks on the markers
    marker = figure['data'][curve]
    customdata = marker['customdata'][point]
    nom_projet = customdata[0]
    mode_implantation = customdata[1]
    objectif_thematique = customdata[2]

    color = marker['marker']['color']

    new_title = html.H4(nom_projet, style={'color': color, 'font-family': 'Oswald', 'margin': '0 0 10px 0', 'padding': '0'})
    
    new_mode = html.P(mode_implantation, style={'margin': '0 0 10px 0', 'padding': '0'})

    if objectif_thematique and objectif_thematique.strip():
        if ';' in objectif_thematique:
            objectifs = [html.Li(obj.strip()) for obj in objectif_thematique.split(';') if obj.strip()]
        elif ',' in objectif_thematique:
            objectifs = [html.Li(obj.strip()) for obj in objectif_thematique.split(',') if obj.strip()]
        else:
            themes = re.split(r'\s+(?=[A-Z])', objectif_thematique)
            objectifs = [html.Li(theme.strip()) for theme in themes if theme.strip()]
        
        if objectifs:
            new_theme = html.Div([
                html.P("Thématique :", style={'margin': '0 0 10px 0', 'padding': '0'}),
                html.Ul(objectifs)
            ])
        else:
            new_theme = None
    else:
        new_theme = None

    new_style = style.copy()
    new_style["display"] = "block"

    return new_title, new_mode, new_theme, new_style