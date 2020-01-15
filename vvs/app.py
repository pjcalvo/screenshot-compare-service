from flask import Flask, render_template
from flask_cors import CORS
from vvs.api.api import api


def create_app():

    # load app instance
    app = Flask(__name__)
    app.register_blueprint(api)
    CORS(app)

    @app.route("/")
    @app.route('/index')
    def index():
        return render_template('index.html', title='Home')

    @app.route("/status")
    def status():
        return {'message': 'Healthy app is healthy!'}, 200

    return app
