from cryptography.fernet import Fernet

key = Fernet.generate_key()
decoded = key.decode('UTF-8')

print('Your key is: {}'.format(decoded))
