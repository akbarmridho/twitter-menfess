# Twitter Autobase

## How it works
This web application will listen to events sent by Twitter Account Activity API including direct message events and process incoming events. If the event satisfy submission requirements, it will be queued and send at certain schedule.

## Features
1. Support more than 15 autobases.
2. Each autobase have different trigger, schedule, interval, and forbidden wordlist.
3. Support word filtering.
4. Support regular message, image, and video.
5. Does not support quoted tweet (yet).
6. Only support one webhook.

## Prerequisites
1. Hosting to run Flask web application.
2. Redis instance.
3. MongoDB database.
4. Twitter developer account with project environment that enable 3 legged OAuth.
5. Sandbox tier or more on Twitter's Account Activity API.
6. Cron jobs or anything that keep `rq_worker.py` or `aps_worker.py` run.

## Install Dependencies
1. Create python virtual environment for this project.
2. Run `pip3 install -r requirements.txt`

## Application Configuration

You should run every script from `script.py` file. Then, choose corresponding option

### Generate Application Key
Save its output to `APP_KEY` environment variable. This key will be use for encrypt and decrypt user OAuth key in database. If the key is lost, you would not able to encrypt and decrypt existing user OAuth key.

### Request OAuth1 Token
Save its output to `TWITTER_OAUTH_KEY` and `TWITTER_OAUTH_SECRET` environment variable. If you run this request on behalf of another user, don't save this key to your environment variable since it will be stored in database.

### Register Webhook
Fill your application host without following slash. Example: www.example.com. Please note that for sandbox tier Twitter Account Activity API only one webhook that is supported. Save webhook_id to `WEBHOOK_ID` environment variable.

### Delete Webhook
Clear enough

### Register User
Make sure registering user have requested their OAuth1 token. Registered user won't automatically subscribed to every account event so you should subscribe manually.

### Delete User
Clear enough

### Subscribe User
Clear enough

### Unubscribe User
Clear enough

## Security
1. Twitter webhook endpoint already meet Twitter CRC requirement.
2. You could verify twitter signature for every incoming events for additional webhook protection. If you want to enable this feature, run `validate_twitter_signature` function in webhook route before process incoming event.
3. Every route in `register_controller.py` **does not** require authentication and authorization. It is a huge security concern so proceed with caution if you really want to use this for production. For basic authentication, you could add `Auth: Bearer sha256=xxx` header for every request and validate it from server side. You could use `generate_decoded_hmac_hash` and `compare_digest` function in encryption module. Hmac hash key is APP_KEY and its message is up to you.
4. User's oauth token key and secret is encrypted in MongoDB database. It required `APP_KEY` for encrypt/decrypt proccess.

## Additional Information
This application use Redis for queue management. If you want to use APScheduler, use `aps_worker.py` and comment out redis enqueuement code in `process_message` function at `autobase.py`.