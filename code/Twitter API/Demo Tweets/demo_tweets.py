import os

import geopandas as gpd
import pymongo
import tweepy
from dotenv import load_dotenv


# Set up twitter API
load_dotenv('../../.env') # .env file in 'code' dir
auth = tweepy.OAuthHandler(os.getenv("CONSUMER_KEY"),
                           os.getenv("CONSUMER_SECRET"))  # app
auth.set_access_token(os.getenv("ACCESS_TOKEN"),
                      os.getenv("ACCESS_TOKEN_SECRET"))  # user
api = tweepy.API(auth)

# Set up MongoDB
client = pymongo.MongoClient('localhost:27017')
db = client["webgefluester"]

# Retrieve district names
plz_shape_df = gpd.read_file('../../OSM/Hamburg.geojson')
names = [district['name'] for district in plz_shape_df.tags]

for district in names:
    tweets = api.search_tweets(q=district, count=3) # beware of rate limit (450 per 15 minutes) but we should increase the count, because I think only the request is limited not the returned amount
    collection = db[district] # new mongo collection
    
    for tweet in tweets:        
        tweet_json = tweet._json
        tweet_json['_id'] = tweet_json.pop('id')  # change name of tweet id so no duplicate tweet is stored
        try:
            collection.insert_one(tweet._json)
        except pymongo.errors.DuplicateKeyError:
            continue

