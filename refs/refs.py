"""
Note: I added h (home) or a (away) to the basketball-reference csv

http://www.basketball-reference.com/referees/2016_register.html
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

def set_plot_params(size):
    SIZE = size
    plt.rc('font', size=SIZE)  
    plt.rc('axes', titlesize=SIZE)  
    plt.rc('axes', labelsize=SIZE)  
    plt.rc('xtick', labelsize=SIZE)  
    plt.rc('ytick', labelsize=SIZE)
    plt.rc('legend', fontsize=SIZE)  
    plt.rc('figure', titlesize=SIZE)
    
def organize_data(filename):
    df = pd.read_csv('2016-refs.csv')
    df = df[df['G']>40]
    df.columns.values
    return df
    
def make_plots(df):
    """
    Various plots where each data point is a given statistic for each ref
    """
    # Plot of average home and away FTA for each ref
    plt.figure()
    plt.scatter(df['hFTA'], df['aFTA'], s=32)
    fig = plt.gcf()
    ax = fig.gca()
    circle = plt.Circle((26, 25), 0.35, fill=False, linewidth=3)
    ax.add_artist(circle)
    plt.xlabel('Home FTA awarded')
    plt.ylabel('Away FTA awarded')
    plt.savefig('plots/FTA.png')
    
    #KDE of FTA awarded
    plt.figure()
    sns.distplot(df['FTA'], rug=True, hist=False)
    plt.title('3 outlier refs')
    plt.xlabel('FTA awarded')
    plt.ylabel('Kernel Density Estimate')
    plt.savefig('plots/FTA_rug.png')
    
    #Plot of all personal fouls for each ref
    plt.figure()
    plt.scatter(df['hPF'], df['aPF'], s=32)
    fig = plt.gcf()
    ax = fig.gca()
    circle = plt.Circle((22.3, 22.2), 0.2, fill=False, linewidth=3)
    ax.add_artist(circle)
    plt.xlabel('Home Personal Fouls')
    plt.ylabel('Away Personal Foulss')
    plt.savefig('plots/PF.png')

    #Plot of personal and shooting fouls for each ref
    plt.figure()
    sns.regplot(df['PF'], df['FTA'], scatter_kws={"s": 60}, ci=False)
    plt.title('Refs that prefer calling shooting fouls')
    fig = plt.gcf()
    ax = fig.gca()
    circle = plt.Circle((41.8, 51), 1, fill=False, linewidth=3)
    plt.xlabel('Personal Fouls')
    plt.ylabel('FTA awarded')
    ax.add_artist(circle)
    plt.savefig('plots/PFvFTA.png')
    

if __name__ == "__main__":
    set_plot_params(22)
    df = organize_data('2016-refs.csv')
    make_plots(df)



