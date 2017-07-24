import os
import pickle
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen

MONTHS = ['october', 'november', 'december', 'january',
          'february', 'march', 'april', 'may']


def get_game_IDs(months=MONTHS):
    """
    Scrape basketball reference game IDs for the 2016-17 season.
    I should probably extend this to make it for any season.

    Args:
        months (list): list of months (str)

    Returns:
        URLS (list): list of basektball reference game IDs
    """
    URLS = []
    for month in months:
        url = ("http://www.basketball-reference.com/"
               "leagues/NBA_2017_games-{month}.html").format(month=month)
        html = urlopen(url)
        soup = BeautifulSoup(html)
        for link in soup.findAll('a'):
            if link.get('href').startswith('/boxscores/201'):
                full_link = link.get('href')
                base_link, extension = os.path.splitext(full_link)
                id = base_link.split('/')[2]
                URLS.append(id)
    return URLS


def get_pbp(game_ID):
    """
    Scrape basketball reference game play-by-play by ID

    Args:
        game_ID (str): bball reference gameID

    Returns: None
        pickles pbp DataFrame to data directory
    """
    url = ('http://www.basketball-reference.com/'
           'boxscores/pbp/{ID}.html').format(ID=game_ID)
    df = pd.read_html(url)[0]
    df.columns = df.iloc[1]
    df = df.drop(df.index[1])
    df['Quarter'] = df.Time.str.extract('(.*?)(?=Q)', expand=False).str[0]
    df['Quarter'] = df['Quarter'].fillna(method='ffill')
    df['ID'] = game_ID
    pickle.dump(df, open("data/{game_ID}.p".format(game_ID=game_ID), "wb"))
    print(game_ID)
    return None


def cache_all_pbp(game_ids):
    for id in game_ids:
        if "{id}.p".format(id=id) not in os.listdir('./data/'):
            get_pbp(id)
        else:
            print('*****', id)
    return None


if __name__ == '__main__':
    ids = get_game_IDs()
    cache_all_pbp(ids)
