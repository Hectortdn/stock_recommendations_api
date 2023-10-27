import json
from datetime import date, time, datetime
import concurrent
from repository.index import Repository

repo = Repository()

def configure(app):

    @app.route('/api/stock-chart-line-data', methods=['GET'])
    def get_stock_close_chart_data():
        best_stocks = repo.ranking[:5]

        stock_close_chart_data = []
        for ticker in best_stocks:
            stock_close = json.loads(ticker.get('stockClose'))
            

            min_valor = min(stock_close.values())
            max_valor = max(stock_close.values())

            data_to_chart_formatted = [{'x': date, 'y': round((value - min_valor) / (max_valor - min_valor),2) } for date, value in stock_close.items()]
            stock_close_chart_data.append({"name": ticker.get('ticker'),'data': data_to_chart_formatted})
        return stock_close_chart_data


    @app.route('/api/stock-table-values', methods=['GET'])
    def get_stock_close_table():
        row_table = []

        data_obj = date(2023, 10, 26)
        hora_obj = time(0, 0, 0)

        date_obj = str(datetime.combine(data_obj, hora_obj))  + "-03:00"


        for ticket in repo.tickers  :
            _open, _high, _low, _close = ticket.get('stockValues').get(date_obj, 'NAN')

            
            row_table.append({
                'open':_open,
                "high":_high,
                "low": _low,
                "date": data_obj,
                "close": _close,
                "price": ticket.get("price"),
                "ticket": ticket.get("ticker"),
                "percentageVariation": ticket.get("percentageVariation"),
                })

        return row_table


    @app.route('/api/stock-suno-indicators', methods=['GET'])
    def get_indicators():
        return {}
        # tickers = [item.get('ticker') for item in repo.ranking]

        # with concurrent.futures.ThreadPoolExecutor() as executor:
        #     results = executor.map(get_suno_indicators_ticker, tickers)

        # return [json.loads(result) for result in results if result ]
        
        
