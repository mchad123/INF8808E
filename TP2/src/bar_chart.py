'''
    Contains some functions related to the creation of the bar chart.
    The bar chart displays the data either as counts or as percentages.
'''

import plotly.graph_objects as go
import plotly.io as pio

from hover_template import get_hover_template
from modes import MODES, MODE_TO_COLUMN


def init_figure():
    '''
        Initializes the Graph Object figure used to display the bar chart.
        Sets the template to be used to "simple_white" as a base with
        our custom template on top. Sets the title to 'Lines per act'

        Returns:
            fig: The figure which will display the bar chart
    '''
    fig = go.Figure()

    # TODO : Update the template to include our new theme and set the title

    fig.update_layout(
        template=pio.templates['custom_theme'],
        title='Lines per act',
        dragmode=False,
        barmode='relative'
    )

    return fig


def draw(fig, data, mode):
    '''
        Draws the bar chart.

        Arg:
            fig: The figure comprising the bar chart
            data: The data to be displayed
            mode: Whether to display the count or percent data.
        Returns:
            fig: The figure comprising the drawn bar chart
    '''
    fig = go.Figure(fig)  # conversion back to Graph Object
    fig.data = [] 
    
    y_col = MODE_TO_COLUMN[mode]
    
    print("////////////////////////////////////////////////////")
    print(data.head())  # Confirm content
    print(data.columns) # Confirm column names
      # Create one bar trace per player
    for player in data['Player'].unique():
        player_data = data[data['Player'] == player]
        fig.add_trace(go.Bar(
            x=player_data['Act'],
            y=player_data[y_col],
            name=player
        ))

    # Update y-axis title based on mode
    y_title = "Number of Lines" if mode == "count" else "Percentage of Lines (%)"
    fig.update_layout(
        yaxis_title=y_title,
        xaxis_title="Act"
    )

    # TODO : Update the figure's data according to the selected mode
    return fig


def update_y_axis(fig, mode):
    '''
        Updates the y axis to say 'Lines (%)' or 'Lines (Count) depending on
        the current display.

        Args:
            mode: Current display mode
        Returns: 
            The updated figure
    '''
    # TODO : Update the y axis title according to the current mode
    y_title = 'Lines (Count)' if mode == 'count' else 'Lines (%)'
    
    fig.update_layout(
        yaxis_title=y_title
    )

    return fig
    