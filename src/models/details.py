

#Models

def best_stocks(tickers):
    tickers_data = tickers[:5]

    stock_close_normalized = []

    for ticker in tickers_data:
        stock_close = {item['date']:item['close'] for item in  ticker.get('stockValues')}
        
        min_valor = min(stock_close.values())
        max_valor = max(stock_close.values())

        data_to_chart_formatted = [{'x': date, 'y': round((value - min_valor) / (max_valor - min_valor),2) } for date, value in stock_close.items()]
        
        
        stock_close_normalized.append({
            'papel'                : ticker['papel'],
            'sector'               : ticker['sector'],
            'cotacao'              : ticker['cotacao'],
            'percentageVariation'  : ticker['percentageVariation'],
            'chartNormalizedClose' : data_to_chart_formatted,
            })

    return stock_close_normalized