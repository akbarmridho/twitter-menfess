import requests

host = input('Enter webservice host url: (www.somesite.com)')
name = input('Enter registered user name: ')
endpoint = '/user/subscribe'

full_url = host + endpoint

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

response = requests.post(full_url, headers=headers, json={'name': name})

if response.ok:
    print('Successfully subscribe user')
else:
    print('Failed to subscribe user')
    print(response.text)
