import concurrent
from repository.index import Repository
from actions.dashboard.index import ranking_greenblatt_magic_formula, format_data_to_candlestick

repo = Repository()

def configure(app):

    @app.route('/api/stock-ranking', methods=['GET'])
    def get_stock_ranking():
         if len(repo.ranking) == 0:
             ranking = ranking_greenblatt_magic_formula(repo.tickers)
             repo.set_ranking(ranking)
             return ranking
         return repo.ranking

    @app.route('/api/stock-candlestick-data', methods=['GET'])
    def get_stock_candlestick_data():
        chart_data = []

        for ticker in repo.tickers:
            stock_close = ticker.get('stockClose')
            stock_values = ticker.get('stockValues')

            with concurrent.futures.ThreadPoolExecutor(2) as executor:
                 chart_close = executor.submit(format_data_to_candlestick, stock_close).result()
                 chart_values = executor.submit(format_data_to_candlestick, stock_values).result()
            
            chart_data.append({
                "chartClose":chart_close,
                "chartValues":chart_values,
                "type": ticker.get("type"),
                "price":ticker.get("price"),
                "ticker": ticker.get('ticker'),
                "percentageVariation":ticker.get("percentageVariation"),
            })

        return chart_data


            

         