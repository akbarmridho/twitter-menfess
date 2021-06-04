from flask import Flask, request
from application import get_config, connect
from application.controllers import twitter_controller, register_controller
import sys
import logging
import os


def create_app():

    app = Flask(__name__)

    app.config.from_object(get_config())

    connect()

    app.register_blueprint(twitter_controller.bp)
    app.register_blueprint(register_controller.bp)

    @app.route('/')
    def home():
        return "<p>Hello World</p>"

    if 'DYNO' in os.environ:
        app.logger.addHandler(logging.StreamHandler(sys.stdout))
        app.logger.setLevel(logging.ERROR)

    return app


if __name__ == '__main__':
    create_app().run()
