import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import urllib2
from bs4 import BeautifulSoup
import re

teams = ['ATL', 'BOS', 'BRK', 'CHO', 'CHI', 'CLE', 'DAL', 'DEN', 'HOU',
         'DET', 'GSW', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN',
         'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS',
         'TOR', 'UTA', 'WAS'
        ]

def get_record(team, year):
    url = 'http://www.basketball-reference.com/teams/' + team + '/' + str(year) + '.html'
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page)
    soup.prettify()
    for anchor in soup.findAll('p'):
        if 'Record:' in anchor.get_text():
            match = re.search(':(.*),', anchor.get_text())
            record = match.group(1)
            record = record.split('-')
            wins = record[0]
            loses = record[1]
    return (int(wins), int(loses))
    
def set_plot_params(size):
    SIZE = size
    plt.rc('font', size=SIZE)  
    plt.rc('axes', titlesize=SIZE)  
    plt.rc('axes', labelsize=SIZE)  
    plt.rc('xtick', labelsize=SIZE)  
    plt.rc('ytick', labelsize=SIZE)
    plt.rc('legend', fontsize=SIZE) 

def get_data(drafts, draft_years):
    data = []
    for year in draft_years:
        tanker = drafts[drafts['Year'] == year]['Team'].values[0]
        counter = 0
        for  following_year in range(year, 2017):
            team = tanker + str(year)
            season = following_year
            years_since = counter
            try:
                record = get_record(tanker, following_year)
            except:
                if tanker == "BRK":
                    record = get_record('NJN', following_year)
                elif tanker == 'CHA':
                    record = get_record('CHH', following_year)
            winperc = float(record[0]) / sum(record)
            data.append([team, season, years_since, winperc])
            counter += 1
            if counter > 10:
                break
        return data
        
def make_plots(df):
    relative_points = pd.DataFrame()  
    for team in df.team.unique():
        team_data = df[df.team == team]
        starting_point = team_data[team_data['years_since'] == 0]['win%']
        team_data['relative%'] = team_data['win%'] - float(starting_point)
        relative_points = relative_points.append(team_data)
        
    plt.figure()
    sns.boxplot(relative_points['years_since'], relative_points['relative%'])
    plt.xlabel('Years since obtaining 1st pick')
    plt.ylabel('Win Percent difference')
    plt.title('10 year trajectory after obtaining 1st pick')
    
    plt.figure()
    df['Playoffs'] = df['win%'] > 0.5
    df.groupby('years_since').mean()['Playoffs'].plot(kind='bar')
    plt.xlabel('Years since obtaining 1st pick')
    plt.ylabel('Percentage of teams making playoffs')
    plt.title('10 year trajectory after obtaining 1st pick')

if __name__ == "__main__":
    set_plot_params(22)
    draft_years = range(1990, 2012)
    drafts = pd.read_csv('drafts.csv')
    data = get_data(drafts, draft_years)
    cols = ['team', 'season', 'years_since', 'win%']
    df = pd.DataFrame(data = data, columns = cols)
    make_plots(df)

