from flask import Flask
import flask_restful

from vvs.api.api import api

def create_app():

    # load app instance
    app = Flask(__name__)
    app.register_blueprint(api)

    @app.route("/")
    def index():
        return 'Hello there! Welcome to visual validation service!'

    @app.route("/status")
    def status():
        return {'message': 'Healthy app is healthy!'}, 200

    return app
