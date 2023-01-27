import bs4 as bs
import datetime as dt
import os
import pandas as pd
from pandas_datareader import data as pdr
import pickle
import requests
import yfinance as yfin
from tqdm import tqdm
yfin.pdr_override()

def save_sp500_tickers():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    categories = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text.strip()
        category = row.findAll('td')[3].text.strip()
        tickers.append(ticker)
        categories.append(category)
    df = pd.DataFrame.from_dict({'ticker': tickers, 'category': categories}).set_index('ticker')
    df.to_csv('data/sp500_companies.csv')
    with open("data/sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)
    return tickers

def get_data_from_yahoo(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)
    if not os.path.exists('data/stock_dfs'):
        os.makedirs('data/stock_dfs')
    tickers.append('^GSPC')
    start = dt.datetime(2009,1,1)
    end = dt.datetime(2022,12,31)
    for ticker in tqdm(tickers):
        # just in case your connection breaks, we'd like to save our progress!
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = pdr.get_data_yahoo(ticker, start, end)
            df.reset_index(inplace=True)
            df.set_index("Date", inplace=True)
            # df = df.drop("Symbol", axis=1)
            df.to_csv('data/stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))

get_data_from_yahoo(True)