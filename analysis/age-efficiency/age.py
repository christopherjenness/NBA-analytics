import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
import time
import pickle
import seaborn as sns
import matplotlib.pyplot as plt

def load_cached_dfs():
    dfs = []
    for fname in os.listdir("scrapper/data/"):
        df =  pickle.load(open("scrapper/data/" + fname, "rb"))
        df['URL'] = fname
        dfs.append(df)
    return dfs

def clean_dfs(dfs):
    df = pd.concat(dfs)
    df = df[df.Age != '']
    df = df[df.MP != '']
    df = df[df.ORtg != '']
    df = df[df.DRtg != '']
    df[['Age', 'MP', 'ORtg', 'DRtg', 'FGA', 'ORB', 'DRB', 'AST', 'STL', 'BLK', 'TOV', 'PF']] = df[['Age', 'MP', 'ORtg', 'DRtg', 'FGA', 'ORB', 'DRB', 'AST', 'STL', 'BLK', 'TOV', 'PF']].astype(float)
    df['Age'] = df['Age'].astype(int)
    df = df[df['MP'] > 1000]
    return df

def set_plot_params(size):
    SIZE = size
    plt.rc('font', size=SIZE)  
    plt.rc('axes', titlesize=SIZE)  
    plt.rc('axes', labelsize=SIZE)  


def make_plots(df):
    df = df[df['Age'] > 19]
    df = df[df['Age'] < 36]
    ave_df = df.groupby('Age').mean()
    
    set_plot_params(18)
    plt.figure()
    plt.plot(ave_df['ORtg'], label='Offensive Rating')
    plt.plot(ave_df['DRtg'], label='Defensive Rating')
    plt.legend(loc = 8)
    plt.ylabel('Offensive, Defensive Rating')
    plt.xlabel('Age')
    plt.title('As players age, offense increases, defense decreases', y=1.05)
    plt.tight_layout()
    plt.savefig('plots/rating')
    
    
    plt.figure()
    plt.plot(ave_df['TOV'])
    plt.ylabel('TOV per 100 possessions')
    plt.xlabel('Age')
    plt.title('As players age, they commit less turnovers')
    plt.tight_layout()
    plt.savefig('plots/TOV')
    
    plt.figure()
    plt.plot(ave_df['PF'])
    plt.ylabel('Fouls per 100 possessions')
    plt.xlabel('Age')
    plt.title('As players age, they commit less fouls')
    plt.tight_layout()
    plt.savefig('plots/PF')
    
    set_plot_params(22)
    fig, axs = plt.subplots(1, 2, figsize=(18, 6))
    fig.suptitle('As players age, they shoot less and assist more', y=1.05)
    plt.axes(axs[0])
    plt.plot(ave_df['FGA'])
    plt.ylabel('FGA per 100 possessions')
    plt.xlabel('Age')
    plt.axes(axs[1])
    plt.plot(ave_df['AST'])
    plt.ylabel('AST per 100 possessions')
    plt.xlabel('Age')
    plt.tight_layout()
    plt.savefig('plots/FGA')

if __name__ == '__main__':
    dfs = load_cached_dfs()
    df = clean_dfs(dfs)
    make_plots(df)
