from os import environ
from typing import Dict
from flask import request
import hmac
import hashlib
import base64


def webhook_challenge() -> Dict:

    TWITTER_CUSTOMER_SECRET = environ.get('TWITTER_CUSTOMER_SECRET')

    # Create HMAC SHA-256 hash from incoming token and your customer secret
    sha256_hmac: hmac.HMAC = hmac.new(TWITTER_CUSTOMER_SECRET, msg=request.args.get(
        'crc_token'), digestmod=hashlib.sha256())
    sha256_hash_digest = sha256_hmac.digest()

    return {
        'response_token': 'sha256=' + base64.encode(sha256_hash_digest)
    }


def validate_twitter_signature() -> bool:

    to_compare = request.headers['x-twitter-webhooks-signature']

    if not to_compare:
        to_compare = request.headers['X-Twitter-Webhooks-Signature']

    TWITTER_CUSTOMER_SECRET = environ.get('TWITTER_CUSTOMER_SECRET')
    sha256_hmac: hmac.HMAC = hmac.new(
        TWITTER_CUSTOMER_SECRET, msg=request.data, digestmod=hashlib.sha256())
    sha256_hash_digest = sha256_hmac.digest()
    return hmac.compare_digest(to_compare, 'sha256=' + base64.encode(sha256_hash_digest))
