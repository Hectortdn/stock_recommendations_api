from flask import jsonify
import models.dashboard as dsb
from repository.index import Repository


class DashBoardController:

    def __init__(self, repository: Repository):
        self.repository = repository

    
    def stock_ranking(self):
        fundamentus_data = self.repository.fundamentus

        if  fundamentus_data == None:
            return jsonify({
                "message": 'Repositorio vazio!',
                'error': True
            }), 404


        ranking = dsb.ranking_greenblatt(fundamentus_data)

        return jsonify(ranking)

    def stock_correlations(self):
        stock = self.repository.tickers

        if  stock == []:
            return jsonify({
                "message": 'Repositorio vazio!',
                'error': True
            }), 404
        
        corr = dsb.stock_correlations(stock)
        return jsonify(corr)
    

        




    