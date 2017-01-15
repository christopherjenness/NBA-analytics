import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
from scipy.stats import beta

def set_plot_params(size):
    SIZE = size
    plt.rc('font', size=SIZE)  
    plt.rc('axes', titlesize=SIZE)  
    plt.rc('axes', labelsize=SIZE)  
    plt.rc('xtick', labelsize=SIZE)  
    plt.rc('ytick', labelsize=SIZE)
    plt.rc('legend', fontsize=SIZE)  
    plt.rc('figure', titlesize=SIZE)

def organize_data():
    df = pd.read_csv('2016stats.csv')
    df = df[df['3PA'] > 20]
    df['3P%'] = df['3P%']/100
    a = beta.fit(list(df['3P%']),floc=0, fscale=1)[0]
    b =  beta.fit(list(df['3P%']),floc=0, fscale=1)[1]
    df['3PEstimate'] = (df['3PM'] + a) / (df['3PA'] + a + b)
    df['a'] = df['3PM'] + a
    df['b'] = df['3PA'] - df['3PM'] + b
    print('alpha: ' + str(a))
    print('beta: ' + str(b))
    return (df, a, b)

def make_plots(df, a, b):
    plt.figure()
    plt.hist(df['3P%'], bins=30)
    plt.xlabel('3PT %')
    plt.ylabel('Number of Players')
    plt.title('Distribution of 3PT%')
    plt.savefig('plots/3PT%.png')
    
    plt.figure()
    x = np.linspace(0.01, 0.99, 100)
    y = beta.pdf(x, a, b)
    plt.hist(df['3P%'], bins=30, normed=True, label='Emperical')
    plt.plot(x, y, 'k-', lw=2, label='Beta')
    plt.xlabel('3PT %')
    plt.ylabel('Number of Players')
    plt.title('Beta Approximation of 3PT%')
    plt.legend()
    plt.xlim(0.1, 0.7)
    plt.savefig('plots/betaapprox.png')

    plt.figure()
    plt.hist(df['3P%'], bins=30, normed=True, label='Emperical', alpha=0.6)
    plt.hist(df['3PEstimate'], bins =12, alpha=0.6, label='Estimate', normed=True)
    plt.xlabel('3PT %')
    plt.ylabel('Number of Players')
    plt.title('Bayesian Estimation of 3PT%')
    plt.legend()
    plt.savefig('plots/estimation.png')

    plt.figure()
    y1 = beta.pdf(x, a, b)
    y2 = beta.pdf(x, 58.54, 73.47)
    plt.xlim(0.1, 0.7)
    plt.plot(x, y1, 'r--', lw=1, alpha=0.6, label='League\nDistribution')
    plt.plot(x, y2, 'b-', lw=1, alpha=0.6, label='George\nHill')
    plt.xlabel('3PT %')
    plt.ylabel('3PT% Estimate')
    plt.fill_between(x, 0, y2, where= (x>0.36) & (x<0.5285), alpha=0.6)
    plt.title('George Hill \nBayesian Estimation of 3PT%')
    plt.legend()
    plt.savefig('plots/georgehill.png')

df.sort_values('3PEstimate', ascending=False)[['PLAYER',  '3PEstimate', '3P%', '3PA']].head()
if __name__ == "__main__":
    set_plot_params(14)
    df, a, b = organize_data()
    make_plots(df, a, b)
