from scripts.request_oauth import register_oauth
from scripts.delete_user import delete_user
from scripts.delete_webhook import delete_webhook
from scripts.generate_key import generate_key
from scripts.register_user import register_user
from scripts.register_webhook import register_webhook
from scripts.subscribe_user import subscribe_user
from scripts.unsubscribe_user import unsubscribe_user

options = {
    '1': generate_key,
    '2': register_oauth,
    '3': register_user,
    '4': delete_user,
    '5': register_webhook,
    '6': delete_webhook,
    '7': subscribe_user,
    '8': unsubscribe_user
}

print('Available options')
print('1. Generate key')
print('2. Generate oauth key')
print('3. Register user')
print('4. Delete user')
print('5. Register webhook')
print('6. Delete webhook')
print('7. Subscribe user')
print('8. Unsubscribe user')

opt = input('Choose your option: ')

if not opt in options.keys():
    raise Exception('Choose valid option')

options[opt]()
