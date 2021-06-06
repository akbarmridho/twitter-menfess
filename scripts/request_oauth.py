from application.twitter import UserConfig, TweepyAPI  # type: ignore
from tweepy import TweepError  # type: ignore


def register_oauth():
    config = UserConfig('', '')
    client = TweepyAPI(config)

    # get auth url
    try:
        redirect_url = client.auth.get_authorization_url()
    except TweepError:
        print('Failed to get request token')

    print('Visit following url in a web browser and authorize this app to access your twitter account')
    print('Once you are done, copy the PIN that twitter generate and paste it below')
    print(redirect_url)

    verifier_code = input('PIN: ')

    try:
        client.auth.get_access_token(verifier_code)
        oauth_token = client.auth.access_token
        oauth_secret = client.auth.access_token_secret
    except TweepError:
        print('Failed to get access token')

    if oauth_token and oauth_secret:
        me = client.app.me()
        print('Successfully authorize the app. {}'.format(me.screen_name))
        print('Your oauth token is: {}'.format(oauth_token))
        print('Your oauth secret is: {}'.format(oauth_secret))
        print('Please copy and store it in safe storage as it would be needed for user registration')
    else:
        print('Failed to get the key and secret for the user')
