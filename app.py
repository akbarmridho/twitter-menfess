import logging
import os
import sys

from flask import Flask

from application import connect, get_config
from application.controllers import register_controller, twitter_controller


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

        if app.debug:
            app.logger.setLevel(logging.INFO)
        else:
            app.logger.setLevel(logging.ERROR)

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
