import pandas as pd
import seaborn as sns
import urllib2
from bs4 import BeautifulSoup
import re

teams = ['ATL', 'BOS', 'BRK', 'CHO', 'CHI', 'CLE', 'DAL', 'DEN', 'HOU',
         'DET', 'GSW', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN',
         'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS',
         'TOR', 'UTA', 'WAS'
        ]
        
years = range(1990, 2016)
draft_years = range(1990, 2012)
drafts = pd.read_csv('drafts.csv')

data = []
cols = ['team', 'season', 'years_since', 'win%']
df = pd.DataFrame(columns = cols)
for year in draft_years:
    tanker = drafts[drafts['Year'] == year]['Team'].values[0]
    counter = 0
    for  following_year in range(year, 2017):
        team = tanker + str(year)
        season = following_year
        years_since = counter
        print tanker, following_year
        record = get_record(tanker, following_year)
        winperc = float(record[0]) / sum(recrod)
        data.append([team, season, years_since, winperc])
        counter += 1
        print data
    

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








