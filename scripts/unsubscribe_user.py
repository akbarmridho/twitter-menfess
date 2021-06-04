import requests

host = input('Enter webservice host url: (www.somesite.com)')
name = input('Enter registered user name: ')
endpoint = '/user/unsubscribe/{}'.format(name)

full_url = host + endpoint

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

response = requests.delete(full_url, headers=headers)

if response.ok:
    print('Successfully unsubscribe user')
else:
    print('Failed to unsubscribe user')
    print(response.text)