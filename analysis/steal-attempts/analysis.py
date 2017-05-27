import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data():
    general_df = pd.read_csv('data/2017general.csv', encoding='latin')
    general_df = general_df.rename(columns={general_df.columns.values[0]:'PLAYER'})
    hustle_df = pd.read_csv('data/2017hustle.csv', encoding='latin')
    df = pd.merge(general_df, hustle_df, how='left', on='PLAYER')
    df = df.fillna(0)
    return df

def set_plot_params(size):
    SIZE = size
    plt.rc('font', size=SIZE)
    plt.rc('axes', titlesize=SIZE)
    plt.rc('axes', labelsize=SIZE)
    return None

def make_plots():
    plt.figure()
    plt.scatter(df['DEFLECTIONS'], df['STL'], alpha=0.8)
    plt.xlabel('Total Deflections')
    plt.ylabel('Total Steals')
    plt.text(205, 55, 'Kelly Oubre', size=12)
    plt.xlim(0)
    plt.ylim(0)
    plt.savefig('plots/scatter')
    return None

if __name__ == '__main__':
    df = load_data()
    set_plot_params(16)
    make_plots()
