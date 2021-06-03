from dotenv import load_dotenv
from os import getenv
from cryptography.fernet import Fernet


class Encryption:
    key: bytes
    crypter: Fernet

    def __init__(self):
        self.key = bytes(getenv('APP_KEY'), 'utf-8')
        self.crypter = Fernet(self.key)

    def encrypt(self, value: str):
        return self.crypter.encrypt(value.encode('utf-8')).decode('utf-8')

    def decrypt(self, value: str):
        return self.crypter.decrypt(value.encode('utf-8')).decode('utf-8')
