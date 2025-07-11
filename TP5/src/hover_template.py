'''
    Provides the templates for the tooltips.
'''


def map_base_hover_template():
    '''
        Sets the template for the hover tooltips on the neighborhoods.

        The label is simply the name of the neighborhood in font 'Oswald'.

        Returns:
            The hover template.
    '''
    # TODO : Generate the hover template
    return "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style='font-family:Oswald;font-size:16px;'>%{location}</span><extra></extra>"


def map_marker_hover_template(name):
    '''
        Sets the template for the hover tooltips on the markers.

        The label is simply the name of the walking path in font 'Oswald'.

        Args:
            name: The name to display
        Returns:
            The hover template.
    '''
    # TODO : Generate the hover template
    return f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style='font-family:Oswald;font-size:16px;'>{name}</span><extra></extra>"
