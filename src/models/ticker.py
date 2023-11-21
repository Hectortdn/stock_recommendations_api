from services.googleNews import get_google_news

def get_ticker_info(tickerSelected,tickers ):
        for ticker in tickers:
            if ticker['papel'] == tickerSelected:
                 return ticker


def get_ticker_news(ticker):
    ticker_new = get_google_news(ticker)
    return ticker_new