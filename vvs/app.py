from flask import Flask, render_template
import flask_restful

from vvs.api.api import api


def create_app():

    # load app instance
    app = Flask(__name__)
    app.register_blueprint(api)

    @app.route("/")
    @app.route('/')
    def index():
        return render_template('index.html', title='Home')

    @app.route("/status")
    def status():
        return {'message': 'Healthy app is healthy!'}, 200

    return app
