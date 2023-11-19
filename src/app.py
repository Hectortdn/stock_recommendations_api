from flask_cors import CORS
from flask import  Flask, request

from repository.index import Repository
from routes.blueprint import blueprint

repo = Repository()

app = Flask(__name__)


app.register_blueprint(blueprint)


cors = CORS(app, resources={r"/*": {"origins": "*"}})

if __name__ == '__main__':
    print(20 * '-' + ' STARTING SERVER ' + 20 * '-')

    app.run(port=3000, host='localhost', debug=True)
