import pickle
import os
from collections import defaultdict
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def load_data(filename):
    df = pickle.load(open('scraper/data/{filename}'.format(filename=filename),
                          'rb'))
    df = df.fillna(False)
    team1, team2 = df.columns.values[[1, 5]]
    df.columns.values[2] = team1 + '-PTS'
    df.columns.values[4] = team2 + '-PTS'
    return df, team1, team2


def add_results(df, team1, team2, timeout_dict):
    timeouts = df[df[team1].str.contains('full timeout')
                  .fillna(False)].index.tolist()
    for timeout in timeouts:
        outcome = False
        row = timeout
        while (df.iloc[row].str.contains('enters').sum() > 0) or \
              (df.iloc[row].str.contains('free throw').sum() > 0):
            row += 1
        if df.iloc[row][5]:
            outcome = np.NaN
            continue
        while (not df.iloc[row][2]) and (not df.iloc[row][5]):
            if int(row) == int(df.shape[0]) - 1:
                break
            row += 1
        if df.iloc[row][2]:
            outcome = True
        timeout_dict[team1].append(outcome)

    timeouts = df[df[team2].str.contains('full timeout')
                  .fillna(False)].index.tolist()
    for timeout in timeouts:
        outcome = False
        row = timeout
        while (df.iloc[row].str.contains('enters').sum() > 0) or \
              (df.iloc[row].str.contains('free throw').sum() > 0):
            row += 1
        if df.iloc[row][1]:
            outcome = np.NaN
            continue
        while (not df.iloc[row][4]) and (not df.iloc[row][1]):
            if int(row) == int(df.shape[0]) - 1:
                break
            row += 1
        if df.iloc[row][4]:
            outcome = True
        timeout_dict[team2].append(outcome)

    return timeout_dict


def add_defensive_results(df, team1, team2, timeout_dict):
    timeouts = df[df[team1].str.contains('full timeout')
                  .fillna(False)].index.tolist()
    for timeout in timeouts:
        outcome = False
        row = timeout
        while (df.iloc[row].str.contains('enters').sum() > 0) or \
              (df.iloc[row].str.contains('free throw').sum() > 0):
            row += 1
        if df.iloc[row][5]:
            outcome = np.NaN
            continue
        while (not df.iloc[row][2]) and (not df.iloc[row][5]):
            if int(row) == int(df.shape[0]) - 1:
                break
            row += 1
        if df.iloc[row][2]:
            outcome = True
        timeout_dict[team2].append(outcome)

    timeouts = df[df[team2].str.contains('full timeout')
                  .fillna(False)].index.tolist()
    for timeout in timeouts:
        outcome = False
        row = timeout
        while (df.iloc[row].str.contains('enters').sum() > 0) or \
              (df.iloc[row].str.contains('free throw').sum() > 0):
            row += 1
        if df.iloc[row][1]:
            outcome = np.NaN
            continue
        while (not df.iloc[row][4]) and (not df.iloc[row][1]):
            if int(row) == int(df.shape[0]) - 1:
                break
            row += 1
        if df.iloc[row][4]:
            outcome = True
        timeout_dict[team1].append(outcome)

    return timeout_dict


def analyze_all(defense=False):
    timeout_dict = defaultdict(list)
    for fname in os.listdir('./scraper/data'):
        df, team1, team2 = load_data(fname)
        if defense:
            timeout_dict = add_defensive_results(df, team1,
                                                 team2, timeout_dict)
        else:
            timeout_dict = add_results(df, team1,
                                       team2, timeout_dict)
    return timeout_dict


def make_plots():
    results = analyze_all()

    conversion_dict = {}
    for team in results.keys():
        conversion_dict[team] = (np.sum(results[team]) / len(results[team]))

    df = pd.DataFrame.from_dict(conversion_dict, orient='index')
    df.columns = ['Conversion Percentage']
    df = df.sort_values('Conversion Percentage')

    sns.barplot(df.index, df['Conversion Percentage'], color='seagreen')
    plt.ylabel('Timeout Conversion Percentage')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.ylim(0.3, 0.5)
    plt.savefig('plots/teams')

    defensive_results = analyze_all(defense=True)
    conversion_dict = {}
    for team in defensive_results.keys():
        conversion_dict[team] = 1.0 - \
                                (np.sum(defensive_results[team]) /
                                 len(defensive_results[team]))

    df_def = pd.DataFrame.from_dict(conversion_dict, orient='index')
    df_def.columns = ['Conversion Percentage']
    df_def = df_def.sort_values('Conversion Percentage')

    sns.barplot(df_def.index, df_def['Conversion Percentage'],
                color='seagreen')
    plt.ylabel('Post-Timeout Defensive Stop Percentage')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.ylim(0.45)
    plt.savefig('plots/def')


if __name__ == '__main__':
    make_plots()
