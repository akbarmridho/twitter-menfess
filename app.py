from flask import Flask, request
from application import get_config
from application.twitter import webhook_challenge, validate_twitter_signature
from application.controllers import twitter_controller


def create_app():

    app = Flask(__name__)

    app.config.from_object(get_config())

    app.register_blueprint(twitter_controller.bp)

    @app.route('/')
    def home():
        return "<p>Hello World</p>"

    return app


if __name__ == '__main__':
    create_app().run()
