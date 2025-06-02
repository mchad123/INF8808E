'''
    Provides the templates for the tooltips.
'''


def get_heatmap_hover_template():
    '''
        Sets the template for the hover tooltips in the heatmap.

        Contains three labels, followed by their corresponding
        value, separated by a colon : neighborhood, year and
        trees planted.

        The labels are font 'Roboto Slab' and bold. The values
        are font 'Roboto' and regular weight.
    '''
    # TODO : Define and return the hover template
    return (
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style='font-family:Roboto Slab; font-weight:bold; color:black; padding-left: 30px;'>Neighborhood:</span> "
        "<span style='font-family:Roboto; font-weight:normal; color:black;'>%{y}</span><br>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style='font-family:Roboto Slab; font-weight:bold; color:black;'>Year:</span> "
        "<span style='font-family:Roboto; font-weight:normal; color:black;'>%{x}</span><br>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style='font-family:Roboto Slab; font-weight:bold; color:black;'>Trees planted:</span> "
        "<span style='font-family:Roboto; font-weight:normal; color:black;'>%{z}</span>"
        "<extra></extra>"
    )
def get_linechart_hover_template():
    '''
        Sets the template for the hover tooltips in the heatmap.

        Contains two labels, followed by their corresponding
        value, separated by a colon : date and trees planted.

        The labels are font 'Roboto Slab' and bold. The values
        are font 'Roboto' and regular weight.
    '''
    # TODO : Define and return the hover template
    return (
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style='font-family:Roboto Slab; font-weight:bold; color:black;'>Date:</span> "
        "<span style='font-family:Roboto; font-weight:normal; color:black;'>%{x}</span><br>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style='font-family:Roboto Slab; font-weight:bold; color:black;'>Trees Planted:</span> "
        "<span style='font-family:Roboto; font-weight:normal; color:black;'>%{y}</span>"
        "<extra></extra>"
    )