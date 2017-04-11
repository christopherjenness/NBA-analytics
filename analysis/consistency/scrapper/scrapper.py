"""
Script to get all box scores for each player in 2016-17 season
"""

import pandas as pd
from urllib2 import urlopen
from bs4 import BeautifulSoup
import os
import time
import pickle


def get_player_urls(year, cache=True):
    """
    Get BR URLs for all players in a given year
    Args:
        year (int): year to get active players
    Returns: list
        list of BR URLs
    """
    url = 'http://www.basketball-reference.com/leagues/NBA_' + \
        str(year) + '_totals.html'
    soup = BeautifulSoup(urlopen(url).read(), "lxml")
    urls = []
    for anchor in soup.findAll('a', href=True):
        if anchor['href'].startswith('/players/') and len(anchor['href']) > 10:
            urls.append(anchor['href'])
    if cache:
        pickle.dump(urls, open("urls.p", "wb"))
    return list(set(urls))


def make_complete_url(baseURL):
    base = os.path.splitext(baseURL)[0]
    URL = 'http://www.basketball-reference.com' + base + '/gamelog/2017'
    return URL


def get_gamelog(baseURL, cache=True):
    url = make_complete_url(baseURL)
    fname = os.path.basename(os.path.splitext(baseURL)[0])
    df = pd.read_html(url)[7]
    if cache:
        pickle.dump(df, open("gamelogs/" + fname + ".p", "wb"))
    return df


def make_all_gamelogs(URLS):
    for url in URLS:
        counter = 0
        while counter < 3:
            try:
                get_gamelog(url)
                break
            except:
                counter += 1
                print(counter, url)

if __name__ == '__main__':
    urls = get_player_urls(2017)
    make_all_gamelogs(urls)
