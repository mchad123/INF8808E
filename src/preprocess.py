'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import pandas as pd
from modes import MODE_TO_COLUMN


def summarize_lines(my_df):
    '''
        Sums each player's total of number of lines and  its
        corresponding percentage per act.

        The sum of lines per player per act is in a new
        column named 'PlayerLine'.

        The percentage of lines per player per act is
        in a new column named 'PlayerPercent'

        Args:
            my_df: The pandas dataframe containing the data from the .csv file
        Returns:
            The modified pandas dataframe containing the
            information described above.
    '''
    # TODO : Modify the dataframe, removing the line content and replacing
    # it by line count and percent per player per act
    grouped = my_df.groupby(['Act', 'Player']).size().reset_index(name='PlayerLine')

    # Calculate the total number of lines per act
    total_lines_per_act = grouped.groupby('Act')['PlayerLine'].transform('sum')

    # Calculate percentage
    grouped['PlayerPercent'] = grouped['PlayerLine'] / total_lines_per_act
    
    print(grouped)

    return grouped



def replace_others(my_df):
    '''
    For each act, keeps the 5 players with the most lines
    throughout the play and groups the other players
    together in a new line labeled 'OTHER'.

    - 'Act': the act name
    - 'Player': either a top-5 player or 'OTHER'
    - 'LineCount': number of lines by the player
    - 'PercentCount': percentage of lines by the player in that act

    Parameters:
        my_df (pd.DataFrame): A DataFrame with columns ['Act', 'Player', 'LineCount']

    Returns:
        pd.DataFrame: A new DataFrame with 'OTHER' representing all non-top-5 players per act
    '''
    # Step 1: Identify top 5 players in the entire play by total line count
    top_players = (
        my_df.groupby('Player')['PlayerLine']
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .index.tolist()
    )

    # Étape 2 : Réorganiser les données acte par acte
    result_rows = []

    for act, group in my_df.groupby('Act'):
        other_count = 0
        other_percent = 0.0

        for _, row in group.iterrows():
            player = row['Player']
            count = row['PlayerLine']
            percent = row['PlayerPercent'] * 100  # Convertir en pourcentage

            if player in top_players:
                result_rows.append({
                    'Act': act,
                    'Player': player,
                    'LineCount': count,
                    'LinePercent': round(percent, 6)
                })
            else:
                other_count += count
                other_percent += percent

        if other_count > 0:
            result_rows.append({
                'Act': act,
                'Player': 'OTHER',
                'LineCount': other_count,
                'LinePercent': round(other_percent, 6)
            })

    print(result_rows)
    return pd.DataFrame(result_rows)



def clean_names(my_df):
    '''
        In the dataframe, formats the players'
        names so each word start with a capital letter.

        Returns:
            The df with formatted names
    '''
    # TODO : Clean the player names
    my_df['Player'] = my_df['Player'].str.title()
    my_df = my_df.sort_values(by='Player').reset_index(drop=True)
    return my_df