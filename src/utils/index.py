import json
import concurrent
import fundamentus
import pandas as pd
import yfinance as yf
from pandas_datareader import data as pdr

# Stores
paperPulpStocksTikers = ["RANI3", "KLBN11", "SUZB3"]
animalProteinTikers = ["BRFS3", "MRFG3", "BEEF3", "JBSS3"]
agriDiverseTikers = ["SOJA3", "CAML3", "SMTO3", "SLCE3", "TTEN3"]
energyTikers = ["RRRP3", "CSAN3", "ENAT3", "PETR4", "PRIO3", "RECV3"]
miningMetalsTikers = ["CBAV3", "CSNA3", "CMIN3",  "FESA4", "GGBR4",  "GOAU4", "PMAM3", "VALE3", "USIM5"]

# Actions Commodities
actions_commodities = {
    "energyStocks": energyTikers,
    "agriDiverseStocks": agriDiverseTikers,
    "miningMetalsStocks": miningMetalsTikers,
    "paperPulpStocks": paperPulpStocksTikers,
    "animalProteinStocks": animalProteinTikers,
}


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



def perc_to_float_fundamentus(val):
    """
    Percent to float
      - replace string in pt-br to float
      - from '45,56%' to 0.4556

    Input:
        (DataFrame, column_name)
    """

    res = val
    res = res.replace( to_replace=r'[%]', value='' , regex=True )
    res = res.replace( to_replace=r'[.]', value='' , regex=True )
    res = res.replace( to_replace=r'[,]', value='.', regex=True )
    res = res.astype(float) / 100

    return res


def rename_cols_fundamentus(data):
    df = pd.DataFrame()

    ## Fix: rename columns
    df['cotacao'  ] = data['Cotação'          ]
    df['pl'       ] = data['P/L'              ]
    df['pvp'      ] = data['P/VP'             ]
    df['psr'      ] = data['PSR'              ]
    df['dy'       ] = data['Div.Yield'        ]
    df['pa'       ] = data['P/Ativo'          ]
    df['pcg'      ] = data['P/Cap.Giro'       ]
    df['pebit'    ] = data['P/EBIT'           ]
    df['pacl'     ] = data['P/Ativ Circ.Liq'  ]
    df['evebit'   ] = data['EV/EBIT'          ]
    df['evebitda' ] = data['EV/EBITDA'        ]
    df['mrgebit'  ] = data['Mrg Ebit'         ]
    df['mrgliq'   ] = data['Mrg. Líq.'        ]
    df['roic'     ] = data['ROIC'             ]
    df['roe'      ] = data['ROE'              ]
    df['liqc'     ] = data['Liq. Corr.'       ]
    df['liq2m'    ] = data['Liq.2meses'       ]
    df['patrliq'  ] = data['Patrim. Líq'      ]
    df['divbpatr' ] = data['Dív.Brut/ Patrim.']
    df['c5y'      ] = data['Cresc. Rec.5a'    ]

    return df


def fundamentus_to_dict_inline(fundamentus_data):
    df_fundamentus = pd.DataFrame(fundamentus_data)
    

    fundamentus_results = []
    for index in df_fundamentus.index:
        df_ticker = df_fundamentus.iloc[index]
      
        ticker_model = {column: df_ticker[column] for column in df_ticker.index}
        fundamentus_results.append(ticker_model)

    return fundamentus_results