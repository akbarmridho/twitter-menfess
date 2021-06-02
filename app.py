from flask import Flask, request
from .app import get_config
from .app.twitter import webhook_challenge, validate_twitter_signature

app = Flask(__name__)

app.config.from_object(get_config())


@app.route('/')
def home():
    return "<p>Hello World</p>"


@app.route('/service/listen', methods=['GET', 'POST'])
def hook():
    if request.method == 'GET':
        return webhook_challenge()
    elif request.method == 'POST':
        if validate_twitter_signature():
            pass
            # process incoming message
