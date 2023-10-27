from flask_cors import CORS
from flask import  Flask, request

from actions.utils.index import get_close_by_tickers
from repository.index import Repository
from routes import dashboard, details

repo = Repository()

app = Flask(__name__)
details.configure(app)
dashboard.configure(app)


cors = CORS(app, resources={r"/*": {"origins": "*"}})

if __name__ == '__main__':
    print(20 * '-' + ' STARTING SERVER ' + 20 * '-')
    repo.set_tickers_data(get_close_by_tickers())
    print(20 * '-' + ' STARTED SERVER ' + 20 * '-')

    app.run(port=3000, host='localhost', debug=True)
