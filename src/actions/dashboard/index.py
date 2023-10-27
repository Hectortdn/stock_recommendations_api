import json
import yfinance as yf
from flask import jsonify
from pandas import DataFrame
from multiprocessing import Process

from actions.utils.index import get_df_fundamentus_papel, get_all_commodities_tickers, get_ticker_data
from repository.index import Repository

repo = Repository()


def ranking_greenblatt_magic_formula(tickers_data):
    commodities_tickers = get_all_commodities_tickers()

    df_fundamentus_papel = get_df_fundamentus_papel(commodities_tickers)

    repo.set_fundamentus(df_fundamentus_papel.to_dict())
    df_greenblatt: DataFrame = df_fundamentus_papel[['Setor','ROE']]

    # Add columns PRICE e PE
    for ticker_info in tickers_data:
      df_greenblatt.at[ticker_info['ticker'], 'pe'] =  ticker_info['pe']
      df_greenblatt.at[ticker_info['ticker'], 'type'] =  ticker_info['type']
      df_greenblatt.at[ticker_info['ticker'], 'price'] =  ticker_info['price']
      df_greenblatt.at[ticker_info['ticker'], 'ticker'] = ticker_info['ticker']
      df_greenblatt.at[ticker_info['ticker'], 'stockClose'] =  json.dumps(ticker_info['stockClose'])
      df_greenblatt.at[ticker_info['ticker'], 'percentageVariation'] =  ticker_info['percentageVariation']

    df_greenblatt = df_greenblatt.loc[df_greenblatt['pe'] > 0]
    
    # Add classification columns
    df_greenblatt['CLS/PE'] = df_greenblatt['pe'].rank(method='min', ascending=False)
    df_greenblatt['CLS/ROE'] = df_greenblatt['ROE'].rank(method='min', ascending=True)
    
    # create column Score
    df_greenblatt['score'] = (df_greenblatt['CLS/PE'] + df_greenblatt['CLS/ROE'])
    
    # sort table by Score (Ranking)
    df_greenblatt = df_greenblatt[['score', 'price', 'stockClose', 'type', 'ticker', 'percentageVariation']]
    df_greenblatt = df_greenblatt.sort_values(by='score', ascending=False)


    return df_greenblatt.to_dict(orient='records')

def format_data_to_candlestick(data_dict):
        result = [{"x": date, "y": value} for date, value in data_dict.items()]
        return result