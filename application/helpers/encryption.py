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
        self.key = bytes(getenv('APP_KEY'), 'utf-8')
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
