from typing import Dict
from flask import request
from .api import config
import hmac
import hashlib
import base64


def webhook_challenge() -> Dict:
    """Twitter regular webhook challenge

    Returns:
        Dict: response token
    """

    crc_token = request.args.get('crc_token')

    if not isinstance(crc_token, str):
        raise Exception('CRC Token not found!')

    # Create HMAC SHA-256 hash from incoming token and your customer secret
    hmac_digest = hmac.digest(key=config.CUSTOMER_SECRET.encode(
        'UTF-8'), msg=crc_token.encode('utf-8'), digest=hashlib.sha256)  # type: ignore

    return {
        'response_token': 'sha256=' + base64.b64encode(hmac_digest).decode('ascii')
    }


def validate_twitter_signature() -> bool:
    """Validate twitter signature every incoming request

    Returns:
        bool: True if valid
    """

    to_compare = request.headers['x-twitter-webhooks-signature']

    if not to_compare:
        to_compare = request.headers['X-Twitter-Webhooks-Signature']

    hmac_digest = hmac.digest(key=config.CUSTOMER_SECRET.encode(
        'UTF-8'), msg=request.data, digest=hashlib.sha256)  # type: ignore

    return hmac.compare_digest(to_compare, 'sha256=' + base64.b64encode(hmac_digest).decode('ascii'))
