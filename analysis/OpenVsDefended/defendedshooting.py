import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df0 = pd.read_csv('data/0-2.csv')
df2 = pd.read_csv('data/2-4.csv')
df4 = pd.read_csv('data/4-6.csv')
df6 = pd.read_csv('data/6.csv')

defended = pd.concat([df0, df2]).groupby('PLAYER').sum()
not_defended = pd.concat([df4, df6]).groupby('PLAYER').sum()

defended = defended[defended['3PA'] > 20]
not_defended = not_defended[not_defended['3PA'] > 20]

defended['3%'] = defended['3PM'] / defended['3PA']
not_defended['3%'] = not_defended['3PM'] / not_defended['3PA']

PLAYERS = list(set(defended.index.values).intersection(not_defended.index.values))

df = defended.join(not_defended, how='inner', lsuffix='def', rsuffix='notdef')
df['PLAYER'] = df.index.values

plt.scatter(df['3%def'], df['3%notdef'])
plt.xlabel('defended')
plt.ylabel('open')

a = df[df['3%def'] < 0.4]
b = a[a['3%notdef']>.3][['PLAYER', '3%def', '3%notdef']].sort_values('3%notdef', ascending=False)