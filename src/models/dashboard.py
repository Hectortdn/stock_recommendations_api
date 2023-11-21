import concurrent
import pandas as pd
from flask import jsonify

from utils.index import get_all_commodities_tickers
from repository.index import Repository
from utils.index import fundamentus_to_dict_inline

#Services
from services.fundamentus import get_fundamentus_result
from services.yfinance import get_yfinance_ticker


repository = Repository()

 
# Utilities
def get_fundamentus_data():
    tickers = get_all_commodities_tickers()
    columns_selected = ['papel','cotacao', 'pl', 'roic', 'roe', 'liq2m', 'patrliq', 'evebit', 'mrgliq']

    try:
        df_fundamentus: pd.DataFrame = get_fundamentus_result()
        df_fundamentus = df_fundamentus[df_fundamentus.index.isin(tickers)] 

        df_fundamentus.reset_index(level=0, inplace=True)
        df_fundamentus.columns.name = None
        df_fundamentus = df_fundamentus[columns_selected]

        return df_fundamentus

    except Exception as error:
        print('Error in get fundamentus data', error)

def get_yfinance_data():
    tickers = get_all_commodities_tickers()
    try:

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(get_yfinance_ticker, tickers)

        return  [result for result in results]

    except Exception as error:
        print('Error in get yfinance data', error)

def get_stock():
    try: 

        if repository.fundamentus == None and repository.yfinance == None:  
            df_fundamentus =  get_fundamentus_data()
            yfinance_results = get_yfinance_data()

            repository.set_yfinance(yfinance_results)
            repository.set_fundamentus(df_fundamentus.to_dict())
        
        fundamentus_results = fundamentus_to_dict_inline(repository.fundamentus)
  
        result = []
        for ticker_info_fdm in fundamentus_results:
            for ticker_info_yf in repository.yfinance:
                if ticker_info_fdm["papel"] == ticker_info_yf["ticker"]:
                    result.append({
                        **ticker_info_yf,
                        **ticker_info_fdm
                    })

        
        repository.set_tickers_data(result)

        return  jsonify({
            "data":result,
            'error': False,
            'message': 'success',
        })

    except Exception as error:

        print("Error in get stock", error)
        return jsonify({"error": "Ocorreu um erro interno no servidor."}), 500
    

# Models 
def ranking_greenblatt(fundamentus_data):

    df_fundamentus = pd.DataFrame(fundamentus_data)

    greater_liquidity = df_fundamentus[df_fundamentus['liq2m'] > 1000000]
    netWorth = greater_liquidity[greater_liquidity['patrliq'] > 0]

    greenblatt_formula = netWorth[['papel', 'roic', 'evebit', 'pl', 'roe', 'cotacao']]

    ev_sort = greenblatt_formula.sort_values(by='evebit')
    ev_sort = greenblatt_formula.reset_index(drop=True)
    ev_sort['ev_sort'] = ev_sort.index
    
    roic_sort = ev_sort.sort_values(by='roic', ascending=False)
    roic_sort = roic_sort.reset_index(drop=True)
    roic_sort['roic_sort'] = roic_sort.index

    df_greenblatt = roic_sort
    df_greenblatt['score'] = (df_greenblatt['ev_sort'] + df_greenblatt['roic_sort'])
    df_greenblatt[['score', 'ev_sort','roic_sort' ]] = df_greenblatt[['score', 'ev_sort','roic_sort' ]].astype('float64')
    df_greenblatt = df_greenblatt.sort_values(by='score')
    df_greenblatt = df_greenblatt.reset_index(drop=True)

    greenblatt_dict = fundamentus_to_dict_inline(df_greenblatt.to_dict()) 


    result = []
    for ticker_info_fdm in greenblatt_dict:
        for ticker_info_yf in repository.yfinance:
            if ticker_info_fdm["papel"] == ticker_info_yf["ticker"]:
                result.append({
                    **ticker_info_yf,
                    **ticker_info_fdm
                })

    repository.set_ranking(result)
    
    return  {
        "data":result,
        'error': False,
        'message': 'success',
    }


def stock_correlations(tickers):

    df_corr = pd.DataFrame()

    for ticker in repository.tickers:
        column = ticker['papel']
        data = ticker['stockValues']

        for item in data:
            df_corr.at[item['date'], column] = item['close']
    
    df_corr = df_corr.corr()

    correlation = {}

    for index in df_corr.index:
        correlation[index] = []
        for column in df_corr.columns: 
            correlation[index].append({'ticker': column, 'correlation': round(df_corr.loc[index, column], 1)})
    
    return correlation