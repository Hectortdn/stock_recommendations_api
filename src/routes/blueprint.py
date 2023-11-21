from flask import Blueprint
from repository.index import Repository
from models.dashboard import get_stock

# Controllers
from controllers.ticker import TickerController  
from controllers.details import DetailsController
from controllers.dashboard import DashBoardController

blueprint = Blueprint('blueprint', __name__)

repository = Repository()

TickerControllers = TickerController(repository=repository)
DetailsControllers = DetailsController(repository=repository)
DashBoardControllers = DashBoardController(repository=repository)
 

# DashBoard Routetros
blueprint.route('/api/stock', methods=['GET'])(get_stock)
blueprint.route('/api/best-stock', methods=['GET'])(DetailsControllers.get_best_stocks)
blueprint.route('/api/stock-ranking', methods=['GET'])(DashBoardControllers.stock_ranking)
blueprint.route('/api/stock/<ticket_name>/news', methods=['GET'])(TickerControllers.get_ticker_news)
blueprint.route('/api/stock/<ticket_name>', methods=['GET'])(TickerControllers.get_ticker_data)
blueprint.route('/api/stock-collations', methods=['GET'])(DashBoardControllers.stock_correlations)