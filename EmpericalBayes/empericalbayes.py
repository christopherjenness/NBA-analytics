import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
from scipy.stats import beta

df = pd.read_csv('2016stats.csv')
df = df[df['3PA'] > 20]
df['3P%'] = df['3P%']/100

plt.hist(df['3P%'], bins=30)

a = beta.fit(list(df['3P%']),floc=0, fscale=1)[0]
b =  beta.fit(list(df['3P%']),floc=0, fscale=1)[1]



x = np.linspace(0.01, 0.99, 100)
y = beta.pdf(x, a, b)
ax.plot(x, beta.pdf(x, a, b), 'r-', lw=5, alpha=0.6, label='beta pdf')

rv = beta(a, b)

plt.hist(df['3P%'], bins=30, normed=True, label='Emperical')
plt.plot(x, rv.pdf(x), 'k-', lw=2, label='Beta')
plt.legend()

df['3PEstimate'] = (df['3PM'] + a) / (df['3PA'] + a + b)

plt.hist(df['3P%'], bins=30, normed=True, label='Emperical', alpha=0.6)
plt.hist(df['3PEstimate'], bins =30, alpha=0.6, label='Estimate')
plt.legend()

df.sort_values('3PEstimate', ascending=False)[['PLAYER',  '3PEstimate', 'a', 'b']]

df['a'] = df['3PM'] + a
df['b'] = df['3PA'] - df['3PM'] + b

x = np.linspace(0.01, 0.99, 100)
y1 = beta.pdf(x, a, b)
y2 = beta.pdf(x, 58.54, 73.47)
plt.plot(x, y1, 'r-', lw=5, alpha=0.6, label='League\nDistribution')
plt.plot(x, y2, 'r-', lw=5, alpha=0.6, label='George\nHill')
plt.legend()






