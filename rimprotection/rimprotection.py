import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

def organize_data(year):
    df = pd.read_csv(str(year) + '-defense.csv')
    df = df[df['RA-FGA'] > 100]
    return df
    
def compare_years(year1, year2):
    df1 = organize_data(year1)
    df2 = organize_data(year2)
    df = pd.merge(df1, df2, on='PLAYER', how='inner')
    df['CHANGED'] = df['TEAM_x'] != df['TEAM_y']
    return df

def set_plot_params(size):
    SIZE = size
    plt.rc('font', size=SIZE)  
    plt.rc('axes', titlesize=SIZE)  
    plt.rc('axes', labelsize=SIZE)  
    plt.rc('xtick', labelsize=SIZE)  
    plt.rc('ytick', labelsize=SIZE)
    plt.rc('legend', fontsize=SIZE)  
    plt.rc('figure', titlesize=20)

set_plot_params(13)

df2017 = organize_data(2017)
df2016 = organize_data(2016)

df = compare_years(2015, 2016)
df['CHANGED'] = df['TEAM_x'] != df['TEAM_y']

diffs = df[df['TEAM_x'] != df['TEAM_y']]
diffs[['PLAYER', 'TEAM_x', 'TEAM_y', 'RA-FG%_x', 'RA-FG%_y']]

plt.scatter(diffs['RA-FG%_x'], diffs['RA-FG%_y'])

plt.scatter(df['RA-FG%_x'], df['RA-FG%_y'], c=df.CHANGED)

plt.figure()
for year in range(2010, 2016):
    df = compare_years(year, year+1)
    plt.scatter(df['RA-FG%_x'], df['RA-FG%_y'], c=df.CHANGED)
plt.show()

plt.figure(figsize=(6, 6))
diffs = pd.DataFrame()
for year in range(2010, 2016):
    df = compare_years(year, year+1)
    df = df[df['TEAM_x'] != df['TEAM_y']]
    diffs = pd.concat([diffs, df])
sns.regplot(diffs['RA-FG%_x'], diffs['RA-FG%_y'], ci=False)
plt.xlim(40, 75)
plt.ylim(40, 75)
plt.xlabel('Year 1 Opponent FG% at rim')
plt.ylabel('Year 2 Opponent FG% at rim')
plt.title('Centers who changed teams')
plt.savefig('plots/consistent.png')
print('r-squared: ', stats.pearsonr(diffs['RA-FG%_x'], diffs['RA-FG%_y'])[0])

plt.figure(figsize=(6, 6))
sames = pd.DataFrame()
for year in range(2010, 2016):
    df = compare_years(year, year+1)
    df = df[df['TEAM_x'] == df['TEAM_y']]
    sames = pd.concat([sames, df])
sns.regplot(sames['RA-FG%_x'], sames['RA-FG%_y'], ci=False)
plt.xlim(40, 75)
plt.ylim(40, 75)
plt.xlabel('Year 1 Opponent FG% at rim')
plt.ylabel('Year 2 Opponent FG% at rim')
plt.title('Centers who stayed on the same team')
plt.savefig('plots/different.png')
print('r-squared: ', stats.pearsonr(sames['RA-FG%_x'], sames['RA-FG%_y'])[0])


    
