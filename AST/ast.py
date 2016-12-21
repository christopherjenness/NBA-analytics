import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('AST.csv')
df2015 = pd.read_csv('AST2015.csv')

plt.scatter(df['PASSES MADE'], df['AST'])

plt.scatter(df2015['AST'], df2015['SECONDARY AST'])
plt.xlabel('Primary Assists')
plt.ylabel('Secondary Assits')

plt.scatter(df2015['AST'], df2015['FT AST'])

plt.scatter(df['PASSES MADE'], df['PASSES RECEIVED'])

plt.scatter(df2015['AST'], df2015['POTENTIAL AST'])

df2015.sort_values('SECONDARY AST',ascending=False ).head()

def set_plot_params(size):
    SIZE = size
    plt.rc('font', size=SIZE)  
    plt.rc('axes', titlesize=SIZE)  
    plt.rc('axes', labelsize=SIZE)  
    plt.rc('xtick', labelsize=SIZE)  
    plt.rc('ytick', labelsize=SIZE)
    plt.rc('legend', fontsize=SIZE)  

set_plot_params(22)

df2015 = df2015[df2015.AST > 100]
sns.swarmplot(df2015['POTENTIAL AST']/df2015['AST'])

df[df.AST  >30].sort_values('AST VAL', ascending=False).head(20)

df['AST VAL'] = df['AST PTS'] / df['AST']
plt.scatter(df['AST'], df['AST PTS'])
df.sort_values('AST VAL', ascending=False).head(20)

df2015['potentialper'] = df2015['POTENTIAL AST']/df2015['AST']
df2015.sort_values('potentialper', ascending=False).head()

def threePTs(df):
    AST = df['AST']
    ASTPT = df['AST PTS'] 
    counter = 0
    while AST * 2 < ASTPT:
        counter +=1
        ASTPT -= 3
        AST -= 1
    return counter
    
df['3AST'] = df.apply(threePTs, axis=1)
df['2AST'] = df['AST'] - df['3AST']

plt.scatter(df['2AST'], df['3AST'])
df.sort_values('3AST', ascending=False).head()