from flask import Flask, request
from application import get_config, connect
from application.controllers import twitter_controller


def create_app():

    app = Flask(__name__)

    app.config.from_object(get_config())

    connect()

    app.register_blueprint(twitter_controller.bp)

    @app.route('/')
    def home():
        return "<p>Hello World</p>"

    return app


if __name__ == '__main__':
    create_app().run()
