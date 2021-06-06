import requests


def delete_user():
    host = input('Enter webservice host url: (www.somesite.com)')
    name = input('Enter registered user name: ')
    endpoint = '/user/delete/{}'.format(name)

    full_url = host + endpoint

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    response = requests.delete(full_url, headers=headers)

    if response.ok:
        print('Successfully delete user')
    else:
        print('Failed to delete user')
        print(response.text)
