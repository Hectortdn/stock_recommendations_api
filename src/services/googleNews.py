from GoogleNews import GoogleNews
from datetime import datetime

def get_google_news(ticker):
    if ticker:
        googlenews = GoogleNews(period='1d')
        # googlenews.set_encode('utf-8')
        
        search = googlenews.get_news(ticker)
        search = googlenews.results()

        print(search)
        return search
    return {}
