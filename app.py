import logging
import os
import sys

from flask import Flask

from application import connect, get_config
from application.controllers import autobase_controller, twitter_controller


def create_app():

    app = Flask(__name__)

    app.config.from_object(get_config())

    connect()

    app.register_blueprint(twitter_controller.bp)
    app.register_blueprint(autobase_controller.bp)

    @app.route('/')
    def home():
        return "<p>Hello World</p>"

    if 'DYNO' in os.environ:
        app.logger.addHandler(logging.StreamHandler(sys.stdout))

        app.logger.setLevel(logging.INFO)

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
