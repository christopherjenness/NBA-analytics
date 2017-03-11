import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def load_data():
    df = pd.read_csv('drives.csv')
    team_df = df.groupby('TEAM').sum()
    return df, team_df
    
def set_plot_params(size):
    SIZE = size
    plt.rc('font', size=SIZE)  
    plt.rc('axes', titlesize=SIZE)  
    plt.rc('axes', labelsize=SIZE)  
    plt.rc('xtick', labelsize=SIZE)  
    plt.rc('ytick', labelsize=SIZE)
    plt.rc('legend', fontsize=SIZE) 
    
def make_mia_plots(df, team_df):
    fig, axs = plt.subplots(1, 2, figsize=(18, 6))
    plt.axes(axs[0])
    team['PTSperDRIVE'] = team['PTS']/team['DRIVES']
    team = team.sort_values('PTSperDRIVE')
    sns.barplot(x =team.index.values, y=team['PTSperDRIVE'], color='seagreen')
    plt.xticks(rotation=90)
    plt.ylabel('PTS per drive')
    plt.title('Points per drive by team')
    
    plt.axes(axs[1])
    mia = df[df.TEAM == 'MIA']
    mia = mia.sort_values('DRIVES')
    sns.barplot(x = mia['PLAYER'], y=mia['DRIVES'], color='seagreen')
    plt.xticks(rotation=90)
    plt.xlabel('')
    plt.ylabel('Total Drives')
    plt.title('Total drives for MIA players')
    plt.savefig('plots/teams')

plt.scatter(team.DRIVES, team.PTS)

df.sort('FGA')[['PLAYER', 'DRIVES']]

plt.scatter(df.DRIVES, df.TO)
plt.scatter(df.DRIVES, df.PASS)
plt.scatter(df.FGA, df.FTA)
plt.scatter(df.FGA, df.AST)

df.columns.values[2:]

sns.pairplot(df, x_vars = 'DRIVES', y_vars=df.columns.values[2:])
plt.savefig('player')

sns.pairplot(team, x_vars = 'DRIVES', y_vars=team.columns.values[2:])
plt.savefig('team')

team['PTS']/team['DRIVES']

df, team = load_data()

plt.plot(x = team.index, y = (team['PTS']/team['DRIVES']))


fig, axs = plt.subplots(1, 2, figsize=(18, 6))
plt.axes(axs[0])
team['PTSperDRIVE'] = team['PTS']/team['DRIVES']
team = team.sort_values('PTSperDRIVE')
sns.barplot(x =team.index.values, y=team['PTSperDRIVE'], color='seagreen')
plt.xticks(rotation=90)
plt.ylabel('PTS per drive')
plt.title('Points per drive by team')

plt.axes(axs[1])
mia = df[df.TEAM == 'MIA']
mia = mia.sort_values('DRIVES')
sns.barplot(x = mia['PLAYER'], y=mia['DRIVES'], color='seagreen')
plt.xticks(rotation=90)
plt.xlabel('')
plt.ylabel('Total Drives')
plt.title('Total drives for MIA players')
plt.savefig('plots/teams')
