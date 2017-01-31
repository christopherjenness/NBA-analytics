import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

def get_total_shots(df):
    FGA_cols = [zone + '-FGA' for zone in zones]
    attempts = df[FGA_cols]
    return attempts.sum().sum()
    
def get_efg(df):
    twos = [zone + '-FGM' for zone in zones[:3]]
    threes = [zone + '-FGM' for zone in zones[3:]]
    FGM_twos = df[twos]
    FGM_threes = df[threes]
    FGA = get_total_shots(df)
    eFG = (FGM_twos.sum().sum() + 1.5*FGM_threes.sum().sum()) / FGA
    return eFG
    
def get_percent_zone(df, zone):
    FGA = get_total_shots(df)
    zone_FGA = df[zone + '-FGA'].sum()
    return zone_FGA / FGA

def make_zone_plots():
    f, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey=False, figsize=(16,6))
    plt.sca(ax1)
    # Restricted Area
    percent_shots = []
    for partition in partitions:
        percent_shots.append(get_percent_zone(dfs[partition], 'RA'))
    sns.barplot(x=partitions[::-1], y=percent_shots[::-1], color=sns.light_palette("seagreen")[4])
    plt.title('Restricted Area')
    plt.xlabel('Shot Clock')
    plt.ylabel('Percentage of Shots')
    # Mid range
    plt.sca(ax2)
    percent_shots = []
    for partition in partitions:
        percent_shots.append(get_percent_zone(dfs[partition], 'MID'))
    sns.barplot(x=partitions[::-1], y=percent_shots[::-1], color=sns.light_palette("seagreen")[4])
    plt.title('Mid range')
    plt.xlabel('Shot Clock')
    # 3PT
    plt.sca(ax3)
    percent_shots = []
    for partition in partitions:
        percent_shots_top = (get_percent_zone(dfs[partition], 'TOP'))
        percent_shots_left = (get_percent_zone(dfs[partition], 'RIGHT'))
        percent_shots_right = (get_percent_zone(dfs[partition], 'LEFT'))
        percent_shots.append((percent_shots_top + percent_shots_left + percent_shots_right))
    sns.barplot(x=partitions[::-1], y=percent_shots[::-1], color=sns.light_palette("seagreen")[4])
    plt.title('3PT')
    plt.xlabel('Shot Clock')
    fig = plt.gcf()
    fig.suptitle("As the shot clock progresses, \n teams shoot more mid range shots \n and less in the restricted area\n \n", y = 1.15, fontsize=22)
    plt.savefig('plots/zone')

def make_efg_plot():
    efgs = []
    for partition in partitions:
        efgs.append(get_efg(dfs[partition]))
    plt.figure()
    sns.barplot(x=partitions[::-1], y=efgs[::-1], color=sns.light_palette("seagreen")[4])
    plt.xlabel('Shot Clock')
    plt.ylabel('eFG%')
    plt.title('eFG% decreases late in the shot clock')
    plt.savefig('plots/efg')
    
def compare_teams(team1, team2):
    f, (ax1, ax2) = plt.subplots(1, 2, sharey=False, figsize=(10,6))
    plt.sca(ax1)
    for team in [team1, team2]:
        efgs = []
        for partition in partitions:
            df = dfs[partition]
            df = df[df.TEAM == team]
            efgs.append(get_efg(df))
        sns.barplot(x=partitions[::-1], y=efgs[::-1], color=sns.light_palette("seagreen")[4])
        plt.title(team + ' eFG%')
        plt.xlabel('Shot Clock')
        plt.ylabel('eFG%')
        plt.sca(ax2)
    plt.xlabel('Shot Clock')
    plt.ylabel('')
    plt.savefig('plots/compare')
    
def set_plot_params():
    plt.rc('font', size=12)  
    plt.rc('axes', titlesize=18)  
    plt.rc('axes', labelsize=18)  
    plt.rc('xtick', labelsize=12)  
    plt.rc('ytick', labelsize=12)
    plt.rc('legend', fontsize=12)  
    plt.rc('figure', titlesize=18)

partitions = ['0-4', '4-7', '7-15', '15-18', '18-22', '22-24']
lengths = [4, 3, 8, 3, 4, 2]
zones = ['RA', 'PAINT', 'MID', 'LEFT', 'RIGHT', 'TOP']

dfs = {}
for partition in partitions:
    dfs[partition] = pd.read_csv('data/' + partition + '.csv').convert_objects(convert_numeric=True)

set_plot_params()
make_efg_plot()
compare_teams('MIL', 'POR')
make_zone_plots()
