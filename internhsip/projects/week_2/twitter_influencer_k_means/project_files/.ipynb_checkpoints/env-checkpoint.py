import os
from tweepy import OAuthHandler as OAuth, API, Cursor
import pandas as pd

##### load dotenv to expose api keys to app

from dotenv import load_dotenv
load_dotenv()

##### add api keys as specified in environment variable

CONSUMER_KEY = 'API_key'
CONSUMER_SECRET = 'API_secret_key'
ACCESS_TOKEN = 'Access_token'
ACCESS_SECRET = 'Access_token_secret'

##### get keys from environment

CONSUMER_KEY = os.environ.get(CONSUMER_KEY)
CONSUMER_SECRET = os.environ.get(CONSUMER_SECRET)
ACCESS_TOKEN = os.environ.get(ACCESS_TOKEN)
ACCESS_SECRET = os.environ.get(ACCESS_SECRET)

##### set consumer keys

auth = OAuth(CONSUMER_KEY, CONSUMER_SECRET)

##### set access token

auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

##### connect to twitter API

api = API(auth, wait_on_rate_limit=True)

##### test connection

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text) 
    break

search_words = "#wildfires"
date_since= "2018-11-16"  
# Collect tweets
tweets = Cursor(api.search,
              q=search_words,
              lang="en", 
              since=date_since).items(2)
# Iterate and print tweets
for tweet in tweets:
    print(tweet.text)