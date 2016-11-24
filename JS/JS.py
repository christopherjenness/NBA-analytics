import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

SIZE = 26
plt.rc('font', size=SIZE)  # controls default text sizes
plt.rc('axes', titlesize=SIZE)  # fontsize of the axes title
plt.rc('axes', labelsize=SIZE)  # fontsize of the x any y labels
plt.rc('xtick', labelsize=SIZE)  # fontsize of the tick labels
plt.rc('ytick', labelsize=SIZE)  # fontsize of the tick labels
plt.rc('legend', fontsize=SIZE)  # legend fontsize
plt.rc('figure', titlesize=SIZE)

df = pd.read_csv("2017-total.csv")
df = df.fillna(0)
#df = df[df['3P%'] != 0]
#df = df[df['3P%'] != 1]
df = df[df['3PA'] > 7]

ybar = df['3P%'].mean()
yvar = df['3P%'].var() * len(df)
phat = df['3P'].sum() / df['3PA'].sum()
df['sigma'] = df['3P%'] * (1 - df['3P%']) / df['3PA']
df['c'] =   1 - (len(df) - 3) * df['sigma'] / ((yvar) )
df['JS'] = ybar + df['c'] * (df['3P%'] - ybar)

df.hist('3P%', bins=30, alpha=0.5, label="3P%")
plt.xlim(0, 1)
plt.xlabel('3PT%')
plt.ylabel('Players')


plt.hist(df.JS, bins=40, alpha=0.5, label="Estimation")
plt.xlim(0, 1)
plt.title('James-Stein Estimation')
plt.xlabel('3PT% prediction')
plt.ylabel('Players')
plt.legend()

