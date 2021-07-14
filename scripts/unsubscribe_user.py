import requests


def unsubscribe_user():
    host = input('Enter webservice host url: (www.somesite.com): ')
    name = input('Enter registered user name: ')
    endpoint = f'/api/users/{name}/subscription'

    full_url = host + endpoint

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    response = requests.delete(full_url, headers=headers)

    if response.ok:
        print('Successfully unsubscribe user')
    else:
        print('Failed to unsubscribe user')
        print(response.text)
