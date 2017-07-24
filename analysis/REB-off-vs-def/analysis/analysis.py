import pickle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict

def load_data(filename):
    df = pickle.load(open('../scraper/data/{filename}'.format(filename=filename),
                          'rb'))
    df = df.fillna(False)
    team1, team2 = df.columns.values[[1, 5]]
    df.columns.values[2] = team1 + '-PTS'
    df.columns.values[4] = team2 + '-PTS'
    return df, team1, team2


def extract_reb_counts(df, team1, team2, points, team):
    if team == 1:
        indices = df.loc[df[team1].str.contains('misses ' + str(points))
                         .fillna(False)].index
        team_def = df.iloc[indices][team2].str.startswith('Defensive').sum()
        team_off = df.iloc[indices][team1].str.startswith('Offensive').sum()
    else:
        indices = df.loc[df[team2].str.contains('misses ' + str(points))
                         .fillna(False)].index
        team_def = df.iloc[indices][team1].str.startswith('Defensive').sum()
        team_off = df.iloc[indices][team2].str.startswith('Offensive').sum()
    if type(team_def) != int:
        team_def = 0
    if type(team_off) != int:
        team_off = 0
    return (team_def, team_off)

def analyze_all():
    twos_dict = {}
    threes_dict = {}
    for fname in os.listdir('../scraper/data'):
        df, team1, team2 = load_data(fname)
        if team1 not in twos_dict:
            twos_dict[team1] = [0, 0]
        if team1 not in threes_dict:
            threes_dict[team1] = [0, 0]
        if team2 not in twos_dict:
            twos_dict[team2] = [0, 0]
        if team2 not in threes_dict:
            threes_dict[team2] = [0, 0]
        team_def, team_off = extract_reb_counts(df, team1, team2, 2, 1)
        twos_dict[team1][0] += team_def
        twos_dict[team1][1] += team_off
        team_def, team_off = extract_reb_counts(df, team1, team2, 2, 2)
        twos_dict[team2][0] += team_def
        twos_dict[team2][1] += team_off
        team_def, team_off = extract_reb_counts(df, team1, team2, 3, 1)
        threes_dict[team1][0] += team_def
        threes_dict[team1][1] += team_off
        team_def, team_off = extract_reb_counts(df, team1, team2, 3, 2)
        threes_dict[team2][0] += team_def
        threes_dict[team2][1] += team_off
    return twos_dict, threes_dict

def plot_teams(twos_dict, threes_dict):
    twos_fraction = {}
    threes_fraction = {}
    for team in twos_dict:
        defs, offs = twos_dict[team]
        twos_fraction[team] = offs / (defs + offs)
    for team in threes_dict:
        defs, offs = threes_dict[team]
        threes_fraction[team] = offs / (defs + offs)
    twos = list(twos_fraction.values())
    threes = list(threes_fraction.values())

    df2 = pd.DataFrame(twos, columns=['Fraction'])
    df2['Type'] = 'Two pt miss'
    df3 = pd.DataFrame(threes, columns=['Fraction'])
    df3['Type'] = 'Three pt miss'
    plot_df = df2.append(df3)

    sns.swarmplot(x = plot_df['Type'], y=plot_df['Fraction'], data = plot_df)
    plt.ylabel('Likelihood of offensive rebound')
    plt.xlabel('')
    plt.title('Teams are more likely to offensive rebound 2 pt misses',
              loc='left')
    plt.savefig('../plots/off-rebs')

twos_dict, threes_dict = analyze_all()
plot_teams(twos_dict, threes_dict)



