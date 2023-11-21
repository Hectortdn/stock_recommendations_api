import yfinance as yf
import pandas as pd
from  utils.index  import get_sector_by_ticker, actions_sectors


def get_yfinance_ticker(ticker,period='6mo' ) -> pd.DataFrame:
    ticker_data = yf.Ticker(f'{ticker}.SA')

    typeSector = get_sector_by_ticker(ticker)
    ticker_history = ticker_data.history(period=period).round(2)
    _stock_close = ticker_history['Close']

    stock_values  = [{
        "date" : str(date),
        "open" : row['Open'],
        "high" : row['High'],
        "low"  : row['Low'],
        "close": row['Close'],
        } for date, row in ticker_history.iterrows()]
        
    percentageVariation =  round((((_stock_close.iloc[-1] - _stock_close.iloc[-2]) / _stock_close.iloc[-2]) * 100), 2)

    return {    
        "ticker": ticker,
        "sector": typeSector,
        "stockValues": stock_values,
        "percentageVariation":percentageVariation,
        "sectorLabel": actions_sectors[typeSector],
    }
