import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def organize_data():
    playtypes = ['transition', 'cut', 'offscreen', 'postup', 
                 'handoff', 'PRhandler', 'PRrollman', 
                 'spotup', 'isolation']
                 
    Tms = {
        'Warriors': 'GSW',
        'Rockets': 'HOU',
        'Thunder': 'OKC',
        'Suns': 'PHO',
        'Cavaliers': 'CLE',
        'Bucks': 'MIL',
        'Raptors': 'TOR',
        'Pelicans': 'NOP',
        'Pistons': 'DET',
        'Lakers': 'LAL',
        'Kings': 'SAC',
        'Pacers': 'IND',
        'Bulls': 'CHI',
        'Magic': 'ORL',
        'Nets': 'BRK',
        'Wizards': 'WAS',
        'Nuggets': 'DEN',
        'Heat': 'MIA',
        'Blazers': 'POR',
        'Clippers': 'LAC',
        'Timberwolves': 'MIN',
        'Knicks': 'NYK',
        '76ers': 'PHI',
        'Hawks': 'ATL',
        'Grizzlies': 'MEM',
        'Spurs': 'SAS',
        'Jazz': 'UTA',
        'Hornets': 'CHA',
        'Celtics': 'BOS',
        'Mavericks': 'DAL'
    }
    
    dfs = {}
    df = pd.DataFrame()
    for play in playtypes:
        dfs[play] = pd.read_csv('data/' + play + '.csv')
        dfs[play]['TYPE'] = play
        dfs[play]['FREQ'] = dfs[play]['FREQ'].str[:-1].astype(float)
        dfs[play]['Tm'] = dfs[play]["TEAM"].str.split().str[-1]
        dfs[play]['Tm'] = dfs[play]['Tm'].map(Tms)
        df = pd.concat([df, dfs[play]])
    
    return dfs

def make_plots(dfs):
    # Points per possession for each play -type
    plt.figure()
    order = df.groupby('TYPE').mean()['PPP'].sort_values().index.values
    sns.swarmplot(x='TYPE', y='PPP', data=df, order=order)
    plt.xticks(rotation=45)
    plt.title('Play-types: Points Per Possession')
    plt.savefig('plots/swarm')
    
    # 3x3 scatter of PPP vs FREQ for each play-type
    plt.figure()
    g = sns.FacetGrid(data=df, col='TYPE', col_wrap=3)
    g.map(plt.scatter, 'FREQ', 'PPP').set_titles("{col_name}")
    plt.savefig('plots/PPPscatter')
    
    # Pick and Roll, Roll man scatter plot
    plt.figure()
    data = dfs['PRrollman']
    plt.scatter(dfs['PRrollman']['FREQ'], dfs['PRrollman']['PPP'])
    for label, x, y in zip(data['Tm'], data['FREQ'], data['PPP']):
        if x > 10:
            plt.annotate(
                label,
                xy=(x, y), xytext=(5, 0),
                textcoords='offset points', ha='left', va='top',
                )
    plt.title('Teams that over-use the pick and roll, roll man')
    plt.xlabel('Frequency %')
    plt.ylabel('PPP')
    plt.savefig('plots/PRroll')
    
    # offscreen
    plt.figure()
    data = dfs['offscreen']
    plt.scatter(data['FREQ'], data['PPP'])
    for label, x, y in zip(data['Tm'], data['FREQ'], data['PPP']):
        if y > 1.01:
            plt.annotate(
                label,
                xy=(x, y), xytext=(0, 5),
                textcoords='offset points', ha='left', va='bottom',
                )
    plt.title('Teams that under-use offscreen plays')
    plt.xlabel('Frequency %')
    plt.ylabel('PPP')
    plt.savefig('plots/offscreen')
    
    # isolation
    plt.figure()
    data = dfs['isolation']
    plt.scatter(data['FREQ'], data['PPP'])
    for label, x, y in zip(data['Tm'], data['FREQ'], data['PPP']):
        if x > 10 and y < 0.95:
            plt.annotate(
                label,
                xy=(x, y), xytext=(5, 0),
                textcoords='offset points', ha='left', va='top',
                )
    plt.title('Teams that over-use isolation')
    plt.xlabel('Frequency %')
    plt.ylabel('PPP')
    plt.savefig('plots/isolation')

if __name__ == '__main__':
    dfs = organize_data()
    make_plots(dfs)



