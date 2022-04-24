import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt


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