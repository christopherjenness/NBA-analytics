import os
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
        url = "http://www.basketball-reference.com/leagues/NBA_2017_games-{month}.html".format(month=month)
        html = urlopen(url)
        soup = BeautifulSoup(html)
        for link in soup.findAll('a'):
            if link.get('href').startswith('/boxscores/201'):
                full_link = link.get('href')
                base_link, extension = os.path.splitext(full_link)
                id = base_link.split('/')[2]
                URLS.append(id)
    return URLS

if __name__ == '__main__':
    ids = get_game_IDs()
