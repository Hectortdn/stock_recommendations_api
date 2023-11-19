def get_ticker_info(tickerSelected,tickers ):
        for ticker in tickers:
            if ticker['papel'] == tickerSelected:
                 return ticker
