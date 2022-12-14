import requests
from application.helpers import Encryption
from os import path


def register_user():
    # Set site endpoint
    host = input('Enter webservice host url: (www.somesite.com) ')
    endpoint = '/api/users'
    full_url = host + endpoint

    # Get forbidden words data
    reader = open(path.join(path.dirname(__file__), 'cursed_words.txt'), 'r')
    cursed_words = reader.read().splitlines()
    reader.close()

    chiper = Encryption()

    name = input(
        'Please enter name identifier. Alphanumeric only without spaces. ')
    trigger = input('Please enter autobase trigger: ')
    start = input(
        'Please enter start time for tweet delivery in HH:MM or HH.MM format: ')
    end = input(
        'Please enter start time for tweet delivery in HH:MM or HH.MM format: ')
    interval = int(
        input('Please enter tweet interval for every delivered menfess: '))
    oauth_key = input('Enter your oauth key: ')
    oauth_secret = input('Enter your oauth secret: ')

    data = {
        'name': name,
        'trigger': trigger,
        'oauth_key': chiper.encrypt(oauth_key),
        'oauth_secret': chiper.encrypt(oauth_secret),
        'start': start,
        'end': end,
        'interval': interval,
        'forbidden_words': cursed_words
    }

    headers = {'Content-type': 'application/json',
               'Accept': 'text/plain'}

    response = requests.post(full_url, headers=headers, json=data)

    if response.ok:
        print('User registered')
    else:
        print('Failed to register user')

    print(response.text)
