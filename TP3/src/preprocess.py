'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import pandas as pd


def convert_dates(dataframe):
    '''
        Converts the dates in the dataframe to datetime objects.

        Args:
            dataframe: The dataframe to process
        Returns:
            The processed dataframe with datetime-formatted dates.
    '''
    # TODO : Convert dates
    dataframe['Date_Plantation'] = pd.to_datetime(dataframe['Date_Plantation'])
    return dataframe


def filter_years(dataframe, start, end):
    '''
        Filters the elements of the dataframe by date, making sure
        they fall in the desired range.

        Args:
            dataframe: The dataframe to process
            start: The starting year (inclusive)
            end: The ending year (inclusive)
        Returns:
            The dataframe filtered by date.
    '''
    # TODO : Filter by dates
    dataframe = dataframe[(dataframe['Date_Plantation'].dt.year >= start) & 
                          (dataframe['Date_Plantation'].dt.year <= end)]
    return dataframe


def summarize_yearly_counts(dataframe):
    '''
        Groups the data by neighborhood and year,
        summing the number of trees planted in each neighborhood
        each year.

        Args:
            dataframe: The dataframe to process
        Returns:
            The processed dataframe with column 'Counts'
            containing the counts of planted
            trees for each neighborhood each year.
    '''
    # TODO : Summarize df
    yearly_df = dataframe.groupby([dataframe['Date_Plantation'].dt.year, 'Arrond_Nom']).size().reset_index(name='Counts')
    return yearly_df


def restructure_df(yearly_df):
    '''
        Restructures the dataframe into a format easier
        to be displayed as a heatmap.

        The resulting dataframe should have as index
        the names of the neighborhoods, while the columns
        should be each considered year. The values
        in each cell represent the number of trees
        planted by the given neighborhood the given year.

        Any empty cells are filled with zeros.

        Args:
            yearly_df: The dataframe to process
        Returns:
            The restructured dataframe
    '''
    # TODO : Restructure df and fill empty cells with 0
    heatmap_df = yearly_df.pivot(index='Arrond_Nom', columns='Date_Plantation', values='Counts').fillna(0)
    return heatmap_df


def get_daily_info(dataframe, arrond, year):
    '''
        From the given dataframe, gets
        the daily amount of planted trees
        in the given neighborhood and year.

        Args:
            dataframe: The dataframe to process
            arrond: The desired neighborhood
            year: The desired year
        Returns:
            The daily tree count data for that
            neighborhood and year.
    '''
    # TODO : Get daily tree count data and return
    df_filtered = dataframe[(dataframe['Arrond_Nom'] == arrond) &
                           (dataframe['Date_Plantation'].dt.year == year)]
    
    if df_filtered.empty:
        return pd.DataFrame(columns=['Date_Plantation', 'Counts'])
    
    daily_counts = df_filtered.groupby(df_filtered['Date_Plantation'].dt.date).size().reset_index(name='Counts')
    daily_counts['Date_Plantation'] = pd.to_datetime(daily_counts['Date_Plantation'])
    
    first_date = daily_counts['Date_Plantation'].min()
    last_date = daily_counts['Date_Plantation'].max()
    
    date_range = pd.date_range(start=first_date, end=last_date, freq='D')
    complete_daily_df = pd.DataFrame({'Date_Plantation': date_range})
    
    daily_df = complete_daily_df.merge(daily_counts, on='Date_Plantation', how='left').fillna(0)
    daily_df['Counts'] = daily_df['Counts'].astype(int)
    
    return daily_df
