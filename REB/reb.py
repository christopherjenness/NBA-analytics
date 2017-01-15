import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.patches as mpatches

def organize_data():
    df = pd.read_csv('2016reb.csv')
    df['OKC'] = df.TEAM == 'OKC'
    OKC_players = df[df.OKC==True]
    league_players = df[df.OKC==False]

def make_plots(df):
    """
    Plot of contested vs uncontested rebounds,
    highlighting OKC
    """
    plt.figure()
    plt.scatter(OKC_players.CONTESTEDREB, OKC_players.UNCONTESTEDREB, c=sns.xkcd_palette(['windows blue']), label='OKC')
    plt.scatter(league_players.CONTESTEDREB, league_players.UNCONTESTEDREB, c=sns.xkcd_palette(['amber']), label='League')
    legend = plt.legend(frameon=True, loc=4)
    frame = legend.get_frame()
    frame.set_edgecolor('black')
    plt.xlim(0, 250)
    plt.ylim(0, 350)
    plt.title('OKC Rebounding')
    plt.xlabel('Contested Rebounds')
    plt.ylabel('Uncontested Rebounds')
    plt.text(90, 312, 'Westbrook')
    plt.text(130, 125, 'Adams/Kanter')
    plt.savefig('plots/OKC.png')

if __name__ == '__main__':
    df = organize_data()
    make_plots(df)
