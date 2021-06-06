from cryptography.fernet import Fernet


def generate_key():
    key = Fernet.generate_key()
    decoded = key.decode('UTF-8')

    print('Your key is: {}'.format(decoded))
