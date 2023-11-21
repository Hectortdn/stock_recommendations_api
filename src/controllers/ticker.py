from flask import jsonify
import models.ticker as  tk
from repository.index import Repository


class TickerController:
    def __init__(self, repository: Repository):
        self.repository = repository

    
    def get_ticker_data(self, ticket_name):
        tickers = self.repository.tickers

        if  len(tickers) == 0:
            return jsonify({
                "message": 'Repositorio vazio!',
                'error': True
            }), 404

        ticker_info = tk.get_ticker_info(ticket_name, tickers)
        return ticker_info
    
    def get_ticker_news(self, ticket_name):
        return tk.get_ticker_news(ticket_name)
    




    