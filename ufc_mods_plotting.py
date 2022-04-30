import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt


import plotly.graph_objs as go
from plotly import offline



def plot_by_country(df_fighter_names):
    """Plots number of active UFC fighters by country."""
    df_fighters_country = pd.read_excel('active_fighters_by_country.xlsx',
                               usecols=['FighterName', 'Country']
                               )
    
    df_fighters_country.head(5)
    
    df_country_counts = df_fighters_country.groupby(['Country']).count()
    df_country_counts.head(10)
    
    df_country_counts['Country'] = df_country_counts.index
    df_country_counts.rename(columns={'FighterName': 'CountFighters'},
                            inplace=True)
    df_country_counts.head(5)
    
    
    fig = plt.subplots(figsize=(20,15))
    
    ax = sns.barplot(x='CountFighters', y='Country', data=df_country_counts,
                    palette=sns.color_palette("Dark2")
                    ) 
    
    plt.grid(alpha=0.5)
    ax.tick_params(axis='y', pad=1)
    
    plt.title('Number of Active UFC Fighters by Country', fontsize=20, pad=15)
    plt.xlabel('Number of Fighters', fontsize=16)
    plt.ylabel('Country', fontsize=16)
    
    plt.savefig('Number_of_Active_UFC_Fighters_by_Country.jpg')
    plt.show()
    
# df_fighter_names = pd.read_excel('active_fighters_by_country.xlsx')
# plot_by_country(df_fighter_names)

def individual_top_ten(df_fighter_names):
    """Plots barh chart of top ten active UFC fighters with the most wins on their records."""
    df_individual = pd.read_excel('active_fighters_by_country.xlsx')
    print(df_individual.head(5))
    df_individual.drop(columns=['Unnamed: 0', 'index', 'FighterRecord'], inplace=True)
    print(df_individual.head(5))
    df_indiviual_top_ten = df_individual.sort_values(by=['Wins'], ascending=False)[:10].copy()
    print(df_indiviual_top_ten.shape)
    print(df_indiviual_top_ten.head(10))
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x = df_indiviual_top_ten['Wins'],
        y = df_indiviual_top_ten['FighterName'],
        orientation='h',
        hovertext=df_indiviual_top_ten['Country'],
        marker_color = ('red'),
        marker_pattern_shape="\\"    
        ))

    fig.update_yaxes(autorange='reversed')
    
    fig.update_layout(
        title = {'text': 'Top 10 Active UFC Fighters by Wins', 'x': 0.5, 'yanchor': 'top'},
        xaxis_title='Number of Wins',
        yaxis_title='Fighter Name',
        template='plotly_dark'
        )

    offline.plot(fig, filename='Top_10_Active_UFC_Fighters_by_Wins.html')
    
# df_fighter_names = pd.read_excel('active_fighters_by_country.xlsx')

# individual_top_ten(df_fighter_names)














