import base64
import hashlib
import hmac
from os import getenv

from cryptography.fernet import Fernet


class Encryption:
    """Application encryption tools
    It use APP_KEY as its encrypter key
    If APP_KEY changed, previously encrypted data
    won't be able to decrypted.

    Use with caution
    """
    key: bytes
    crypter: Fernet

    def __init__(self):
        APP_KEY = getenv('APP_KEY')

        if not APP_KEY:
            raise Exception('Cannot load APP_KEY')

        self.key = bytes(APP_KEY, 'utf-8')
        self.crypter = Fernet(self.key)

    def encrypt(self, value: str) -> str:
        """Encrypt data

        Args:
            value (str): value to encrypt

        Returns:
            str: encrypted data
        """
        return self.crypter.encrypt(value.encode('utf-8')).decode('utf-8')

    def decrypt(self, value: str) -> str:
        """Decrypt data

        Args:
            value (str): value to decrypt

        Returns:
            str: decrypted data
        """
        return self.crypter.decrypt(value.encode('utf-8')).decode('utf-8')


def generate_decoded_hmac_hash(key: str, message: str) -> str:
    """Create HMAC SHA-256 hash from incoming key and message

    Args:
        key (str): usually Twitter Custoemr Secret or APP_KEY
        message (str)

    Returns:
        str: sha256 string
    """
    hmac_digest = hmac.digest(key=key.encode(
        'UTF-8'), msg=message.encode('utf-8'), digest=hashlib.sha256)  # type: ignore

    return 'sha256=' + base64.b64encode(hmac_digest).decode('ascii')


def compare_digest(digest: str, another_digest: str) -> bool:
    """Compare two hmac digest

    Equal to a == b

    Args:
        digest (str): sha256=...
        another_digest (str): sha256=...

    Returns:
        bool: True if equal
    """
    return hmac.compare_digest(digest, another_digest)
