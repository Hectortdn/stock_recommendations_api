import json
import concurrent
import fundamentus
import pandas as pd
import yfinance as yf
from pandas_datareader import data as pdr

from actions.commodities.strings import actions_commodities

def get_all_commodities_tickers():
    result = []

    for name, params in actions_commodities.items():
        result.extend(params)
    return result

def get_df_fundamentus_papel(tickers) -> pd.DataFrame:
    fundamentus_papel  = fundamentus.get_papel(tickers)

    return fundamentus_papel


def get_sector_by_ticker(ticker):
    for key, values in actions_commodities.items():
      if ticker in values:
        return key 

def get_close_by_tickers():
    commodities_tickers = get_all_commodities_tickers()

    with concurrent.futures.ThreadPoolExecutor() as executor:
      results = executor.map(get_ticker_data, commodities_tickers)
    
    tickers_data = [result for result in results]

    return tickers_data


def get_ticker_data(ticker, period ='6mo'):
    ticker_data = yf.Ticker(f'{ticker}.SA')

    news = ticker_data.get_news()
    typeSector = get_sector_by_ticker(ticker)
    ticker_history = ticker_data.history(period=period).round(2)
    _stock_close = ticker_history['Close']

    stock_values  = {str(date): list(row[['Open', 'High', 'Low', 'Close']]) for date, row in ticker_history.iterrows()}
    stock_close = {str(date): value for date, value in _stock_close.items()}
    percentageVariation =  round((((_stock_close.iloc[-1] - _stock_close.iloc[-2]) / _stock_close.iloc[-2]) * 100), 2)

    price = ticker_data.info["currentPrice"]
    pe = ticker_data.info.get("trailingPE", 0)

    return {
        "pe": pe,
        "news": news,   
        "price": price,
        "ticker": ticker,
        "type": typeSector,
        "stockClose": stock_close,
        "stockValues": stock_values,
        "percentageVariation":percentageVariation
        
    }
