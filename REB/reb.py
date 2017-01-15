import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('2016reb.csv')

plt.scatter(df.CONTESTEDREB, df.UNCONTESTEDREB)

df.sort_values('UNCONTESTEDREB', ascending=False)[['PLAYER', 'CONTESTEDREB', 'UNCONTESTEDREB']].head()

df.sort_values('CONTESTEDREB', ascending=False)[['PLAYER', 'TEAM', 'CONTESTEDREB', 'UNCONTESTEDREB']].head(25)

df['CHI'] = df.TEAM == 'CHI'
df['OKC'] = df.TEAM == 'OKC'

plt.scatter(df.CONTESTEDREB, df.UNCONTESTEDREB, c=df['OKC'])

for team in df.TEAM.unique():
    plt.figure()
    df[team] = df.TEAM == team
    plt.scatter(df.CONTESTEDREB, df.UNCONTESTEDREB, c=df[team])
    plt.title(team)
    plt.show()
