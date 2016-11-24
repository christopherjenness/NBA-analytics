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
    df = pd.read_csv(filename)
    df = df.fillna(0)
    df = df[df['3PA'] > 7]
    return df
    
def JS_estimation(df):
    """
    Computes James-Stein estimation for dataframe
    Returns original df but with additional columns including 'JS' which is 
        the James-Stein estimation of 3PT percentage.
    """
    ybar = df['3P%'].mean()
    yvar = df['3P%'].var() * len(df)
    df['sigma'] = df['3P%'] * (1 - df['3P%']) / df['3PA']
    df['c'] =   1 - (len(df) - 3) * df['sigma'] / ((yvar) )
    df['JS'] = ybar + df['c'] * (df['3P%'] - ybar)
    return df

def make_plots(df):
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

if __name__ == "__main__":
    set_plot_params(26)
    df = organize_data('2017-total.csv')
    df = JS_estimation(df)
    make_plots(df)
