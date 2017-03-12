import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def load_data():
    df = pd.read_csv('drives.csv')
    team_df = df.groupby('TEAM').sum()
    return df, team_df
    
def set_plot_params(size):
    SIZE = size
    plt.rc('font', size=SIZE)  
    plt.rc('axes', titlesize=SIZE)  
    plt.rc('axes', labelsize=SIZE)  
    plt.rc('xtick', labelsize=SIZE)  
    plt.rc('ytick', labelsize=SIZE)
    plt.rc('legend', fontsize=SIZE) 
    
def make_mia_plots(df, team):
    fig, axs = plt.subplots(1, 2, figsize=(18, 6))
    plt.axes(axs[0])
    team['PTSperDRIVE'] = team['PTS']/team['DRIVES']
    team = team.sort_values('PTSperDRIVE')
    sns.barplot(x = team.index.values, y=team['PTSperDRIVE'], color='seagreen')
    plt.xticks(rotation=90)
    plt.ylabel('PTS per drive')
    plt.title('Points per drive by team')
    
    plt.axes(axs[1])
    mia = df[df.TEAM == 'MIA']
    mia = mia.sort_values('DRIVES')
    names = list(mia['PLAYER'])
    last_names = [name.split(' ')[1] for name in names]
    sns.barplot(x = last_names, y=mia['DRIVES'], color='seagreen', ci=False)
    plt.xticks(rotation=90)
    plt.xlabel('')
    plt.ylabel('Total Drives')
    plt.title('Total drives for MIA players')
    plt.tight_layout()
    plt.savefig('plots/teams')

def make_dragic_plots(df):
    df['Dragic'] = df.PLAYER == 'Goran Dragic'
    dragic = df[df['Dragic'] == True]
    not_dragic = df[df['Dragic'] != True]
    
    fig, axs = plt.subplots(1, 2, figsize=(16, 6))
    plt.axes(axs[1])
    plt.scatter(not_dragic.PASS, not_dragic.AST,  c=sns.xkcd_palette(['amber']), label='League')
    plt.scatter(dragic.PASS, dragic.AST,  c=sns.xkcd_palette(['windows blue']), label='Dragic')
    plt.xlim(0, 350)
    plt.ylim(0, 120)
    plt.ylabel('Passes out of drives')
    plt.xlabel('Assists out of drives')
    plt.title('Dragic is not an exceptional assister')
    
    plt.axes(axs[0])
    plt.scatter(not_dragic.DRIVES, not_dragic.PASS,  c=sns.xkcd_palette(['amber']), label='League')
    plt.scatter(dragic.DRIVES, dragic.PASS,  c=sns.xkcd_palette(['windows blue']), label='Dragic')
    plt.xlim(0)
    plt.ylim(0)
    plt.xlabel('Passes out of drives')
    plt.ylabel('Total drives')
    plt.title('Dragic likes to pass out of drives')
    legend = plt.legend(frameon=True, loc=4)
    frame = legend.get_frame()
    frame.set_edgecolor('black')
    plt.savefig('plots/dragicPASS')
    
    fig, axs = plt.subplots(1, 2, figsize=(16, 6))
    plt.axes(axs[0])
    plt.scatter(not_dragic.DRIVES, not_dragic.FTA,  c=sns.xkcd_palette(['amber']), label='League')
    plt.scatter(dragic.DRIVES, dragic.FTA,  c=sns.xkcd_palette(['windows blue']), label='Dragic')
    plt.xlim(0)
    plt.ylim(0)
    plt.xlabel('Total Drives')
    plt.ylabel('Free throws from drives')
    plt.title('Dragic does not get to the line from drives')
    
    plt.axes(axs[1])
    plt.scatter(not_dragic.DRIVES, not_dragic.FGM,  c=sns.xkcd_palette(['amber']), label='League')
    plt.scatter(dragic.DRIVES, dragic.FGM,  c=sns.xkcd_palette(['windows blue']), label='Dragic')
    plt.xlim(0)
    plt.ylim(0)
    plt.ylabel('Made field goals from drives')
    plt.xlabel('Total drives')
    plt.title('Dragic does not make shots from drives')
    legend = plt.legend(frameon=True, loc=4)
    frame = legend.get_frame()
    frame.set_edgecolor('black')
    plt.savefig('plots/dragicSHOTS')

if __name__ == '__main__':
    df, team = load_data()
    make_mia_plots(df, team)
    make_dragic_plots(df)
