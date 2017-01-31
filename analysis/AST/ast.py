import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def set_plot_params(size):
    SIZE = size
    plt.rc('font', size=SIZE)  
    plt.rc('axes', titlesize=SIZE)  
    plt.rc('axes', labelsize=SIZE)  
    plt.rc('xtick', labelsize=SIZE)  
    plt.rc('ytick', labelsize=SIZE)
    plt.rc('legend', fontsize=SIZE) 

def threePTs(df):
    """
    This function takes an assist data frame and calculates how many
    3PT and 2PT assists each player has.
    """
    AST = df['AST']
    ASTPT = df['AST PTS'] 
    counter = 0
    while AST * 2 < ASTPT:
        counter +=1
        ASTPT -= 3
        AST -= 1
    return counter

def organize_data():
    df = pd.read_csv('AST.csv')
    df['3AST'] = df.apply(threePTs, axis=1)
    df['2AST'] = df['AST'] - df['3AST']
    return df
    
def plot_secondary_assists(df):
    plt.figure()
    plt.scatter(df['AST'], df['SECONDARY AST'], s=60 ,alpha=0.6)
    plt.xlabel('Primary Assists')
    plt.ylabel('Secondary Assits')   
    plt.title('Steph Curry is the king \n of secondary assists')
    plt.xlim(0)
    plt.ylim(0)
    plt.text(190, 65, 'Curry')
    plt.show()
    
def plot_team_secondary_assists(df):
    plt.figure()
    team_AST = df.groupby('TEAM').sum()
    team_AST['SECONDARY AST'].sort_values(ascending=False).plot(kind='bar')
    plt.title('Secondary Assists\n by Team')
    plt.ylabel('Secondary Assists')
    plt.show()
    
def plot_assist_value(df):
    plt.figure()
    plt.scatter(df['2AST'], df['3AST'], s=60, alpha=0.6)
    plt.text(95, 132, 'LeBron')
    plt.text(205, 145, 'Harden')
    plt.xlabel('2PT Assists')
    plt.ylabel('3PT Assists')
    plt.title('Player Assist Value')
    plt.xlim(0, 250)
    plt.ylim(0, 160)
    plt.show()
    
def plot_potential_assists(df):
    plt.figure()
    plt.scatter(df['AST'], df['POTENTIAL AST'], s=60, alpha=0.6)
    plt.xlim(0)
    plt.ylim(0)
    plt.xlabel('Assists')
    plt.ylabel('Potential Assists')
    plt.title('A potential assist is \nworth half an assist')
    plt.show()

if __name__ == 'main':
    set_plot_params(22)
    df = organize_data()
    plot_secondary_assists(df)
    plot_team_secondary_assists(df)
    plot_assist_value(df)  
    plot_potential_assists(df)
