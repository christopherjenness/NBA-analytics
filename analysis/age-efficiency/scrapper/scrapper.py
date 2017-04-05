"""
Script for scraping all player efficiency data from Basketball Reference
"""

import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
import time
import pickle

YEARS = list(range(2000, 2017))

def get_player_urls(year):
    """
    Get BR URLs for all players in a given year
    Args:
        year (int): year to get active players
    Returns: list
        list of BR URLs
    """
    url = 'http://www.basketball-reference.com/leagues/NBA_' + str(year) + '_totals.html'
    soup = BeautifulSoup(urlopen(url).read(), "lxml")
    urls = []
    for anchor in soup.findAll('a', href=True):
        if anchor['href'].startswith('/players/') and len(anchor['href']) > 10:
            urls.append(anchor['href'])
    return list(set(urls))


def get_all_player_urls(year_list, cache=True):
    urls = []
    for year in year_list:
        print(year)
        urls += get_player_urls(year)
    urls = list(set(urls))
    if cache:
        pickle.dump(urls, open("player_urls.p", "wb"))
    return urls
    
def make_full_url(baseurl):
    """
    Helper function to turn base url into full shooting URL for a player
    """
    return 'http://www.basketball-reference.com/' + baseurl 
    


def make_stats_df(baseurl, cache=True):
    url = make_full_url(baseurl)
    html = str(urlopen(url).read())
    html = html.replace('<!--', '')
    html = html.replace('-->', '')
    soup = BeautifulSoup(html)
    
    tables  = soup.findAll("div", {'class': "table_outer_container", })
    cols = [th.getText() for th in tables[3].findAll('th')][:32]
    cols.pop(-3)
    data_rows = tables[3].findAll('tr')[2:]
    player_data = [[td.getText() for td in data_rows[i].findAll('td')] for i in range(len(data_rows))]

    df = pd.DataFrame(player_data, columns=cols)
    df.columns = list(df.columns[1:29]) + ['', 'ORtg', 'DRtg']
    if cache:
        pname = os.path.splitext(os.path.basename(baseurl))[0]
        pickle.dump(df, open('data/' + pname + '.p', "wb"))
    return df

urls = pickle.load(open("player_urls.p", "rb"))

for url in urls:
    counter = 0 
    while counter < 3:
        try:
            df = make_stats_df(url, cache=True)
            break
        except:
            counter += 1
    if counter == 3:
            print("FAILURE", url)


def load_cached_dfs():
    dfs = []
    for fname in os.listdir("data/"):
        df =  pickle.laod(open(fname, "rb"))
        df['URL'] = fname
        dfs.append(df)
    return dfs
    
dfs = load_cached_dfs()
df = pd.concat(dfs)
df = df[df['MP'] > 1000]
ave_df = df.groupby('Age').mean()
sns.barlpot(x='Age' ,y='ORtg')

