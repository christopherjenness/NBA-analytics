import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

SIZE = 18
plt.rc('font', size=SIZE)  # controls default text sizes
plt.rc('axes', titlesize=SIZE)  # fontsize of the axes title
plt.rc('axes', labelsize=SIZE)  # fontsize of the x any y labels
plt.rc('xtick', labelsize=SIZE)  # fontsize of the tick labels
plt.rc('ytick', labelsize=SIZE)  # fontsize of the tick labels
plt.rc('legend', fontsize=SIZE)  # legend fontsize
plt.rc('figure', titlesize=SIZE)



df = pd.read_csv('2016-adv.csv')
df = df[df.MP > 500]
df = df[df['Pos'] != 'PF-C']


plt.hist(df['PER'], bins=25)
plt.xlabel('PER')
plt.ylabel('Players')
plt.title('2015-16 PER Distribution')


df.sort_values('PER').head()
df.sort_values('PER', ascending=True).head(10)[['Player', 'PER']]

df.sort_values('PER', ascending=False).head(20)[['Player', 'PER', 'USG%']]

sns.regplot(df.PER, df['USG%'], ci=False, scatter_kws={"s": 50})
plt.xlabel('PER')
plt.ylabel('Usage %')

sns.swarmplot(x='Pos', y='PER', data=df, order=('PG', 'SG', 'SF', 'PF', 'C'))
plt.title('PER by position')

sns.swarmplot(x='Age', y='PER', data=df)
plt.title('PER by age')





