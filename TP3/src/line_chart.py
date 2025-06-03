'''
    Contains some functions related to the creation of the line chart.
'''
import plotly.express as px
import hover_template
from template import THEME

def get_empty_figure():
    '''
        Returns the figure to display when there is no data to show.

        The text to display is : 'No data to display. Select a cell
        in the heatmap for more information.
    '''
    
    fig = px.scatter()
    fig.update_layout(
        annotations=[
            dict(
                text="No data to display. Select a cell<br>in the heatmap for more information.",
                x=0.5, y=0.5,
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(size=16, family=THEME['font_family'], color=THEME['dark_color'])
            )
        ],
        xaxis=dict(visible=False, showline=False),
        yaxis=dict(visible=False, showline=False),
        dragmode=False,

    )

    return fig


def add_rectangle_shape(fig):
    '''
        Adds a rectangle to the figure displayed
        behind the informational text. The color
        is the 'pale_color' in the THEME dictionary.

        The rectangle's width takes up the entire
        paper of the figure. The height goes from
        0.25% to 0.75% the height of the figure.
    '''
    
    fig.update_layout(
        shapes=[
            dict(
                type="rect",
                xref="paper",
                yref="paper",
                x0=0,
                y0=0.25,
                x1=1,
                y1=0.75,
                fillcolor=THEME['pale_color'],
                layer="below",
                line=dict(width=0, color='rgba(0,0,0,0)')
            )
        ]
    )
    return fig


def get_figure(line_data, arrond, year):
    '''
        Generates the line chart using the given data.

        The ticks must show the zero-padded day and
        abbreviated month. The y-axis title should be 'Trees'
        and the title should indicated the displayed
        neighborhood and year.

        In the case that there is only one data point,
        the trace should be displayed as a single
        point instead of a line.

        Args:
            line_data: The data to display in the
            line chart
            arrond: The selected neighborhood
            year: The selected year
        Returns:
            The figure to be displayed
    '''
    
    non_zero_data = line_data[line_data['Counts'] > 0]
    if len(non_zero_data) == 0:
        return get_empty_figure()
    
    first_date = non_zero_data['Date_Plantation'].min()
    
    first_planting_index = line_data[line_data['Date_Plantation'] == first_date].index[0]
    data_from_first_planting = line_data.iloc[first_planting_index:].copy()
    
    planting_days_count = len(non_zero_data)
    
    if planting_days_count == 1:
        fig = px.scatter(
            non_zero_data,
            x='Date_Plantation',
            y='Counts',
            title=f"Trees planted in {arrond} in {year}"
        )
        
        fig.update_traces(
            marker=dict(
                size=8, 
                color=THEME['line_chart_color'],
                line=dict(width=1, color='white')
            ),
        )
        
        fig.update_xaxes(
            tickformat="%d %b",
            title=""
        )
        
    else:
        fig = px.line(
            data_from_first_planting,
            x='Date_Plantation',
            y='Counts',
            title=f"Trees planted in {arrond} in {year}"
        )
        
        fig.update_traces(
            line=dict(
                color=THEME['line_chart_color'], 
                width=2
            ),
        )
        
        fig.update_xaxes(
            tickformat="%d %b",
            title=""
        )
    
    fig.update_layout(
        title=dict(
            font=dict(
                size=16, 
                family=THEME['accent_font_family'], 
                color=THEME['dark_color']
            )
        ),
        yaxis_title="Trees",
        dragmode=False,
        margin=dict(l=60, r=20, t=60, b=60)
    )
    
    fig.update_xaxes(
        tickfont=dict(size=12, family=THEME['font_family'])
    )
    
    fig.update_yaxes(
        tickfont=dict(size=12, family=THEME['font_family']),
        gridwidth=1
    )

    fig.update_traces(hovertemplate=hover_template.get_linechart_hover_template())
    return fig