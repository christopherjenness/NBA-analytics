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
    df = df[df.MP > 500]
    df = df[df['Pos'] != 'PF-C']
    return df
    
def make_plots(df):
    plt.hist(df['PER'], bins=25)
    plt.xlabel('PER')
    plt.ylabel('Players')
    plt.title('2015-16 PER Distribution')
    plt.show()
    
    sns.regplot(df.PER, df['USG%'], ci=False, scatter_kws={"s": 50})
    plt.xlabel('PER')
    plt.ylabel('Usage %')
    plt.show()
    
    sns.swarmplot(x='Pos', y='PER', data=df, order=('PG', 'SG', 'SF', 'PF', 'C'))
    plt.title('PER by position')
    plt.show()
    
    plt.rc('xtick', labelsize=12)  
    sns.swarmplot(x='Age', y='PER', data=df)
    plt.title('PER by age')
    plt.show()
    plt.rc('xtick', labelsize=26)  

if __name__ == "__main__":
    set_plot_params(26)
    df = organize_data('2016-adv.csv')
    make_plots(df)
    print(df.sort_values('PER', ascending=True).head(10)[['Player', 'PER']])
    print(df.sort_values('PER', ascending=False).head(10)[['Player', 'PER']])
    print(df.sort_values('PER', ascending=False).head(10)[['Player', 'PER', 'USG%']])
