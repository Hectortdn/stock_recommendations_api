from flask import jsonify
import models.details as dt
from repository.index import Repository


class DetailsController:
    def __init__(self, repository: Repository):
        self.repository = repository

    
    def get_best_stocks(self):
         ranking = self.repository.ranking

         if  len(ranking) == 0:
            return jsonify({
                "message": 'Repositorio vazio!',
                'error': True
            }), 404


         best_stocks = dt.best_stocks(ranking)

         return jsonify(best_stocks)
    
    




    