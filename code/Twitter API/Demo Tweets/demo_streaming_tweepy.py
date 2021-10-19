import os
import json
import geopandas as gpd
import pymongo
import tweepy
from dotenv import load_dotenv

# Retrieve district names
plz_shape_df = gpd.read_file('../../OSM/Hamburg.geojson')
names = [district['name'] for district in plz_shape_df.tags]
# Set up twitter API
load_dotenv('../../.env') # .env file in 'code' dir

stream = tweepy.Stream(os.getenv("CONSUMER_KEY"),
                        os.getenv("CONSUMER_SECRET"),
                        os.getenv("ACCESS_TOKEN"),
                        os.getenv("ACCESS_TOKEN_SECRET"))
stream.filter(track = names, languages = "de")
output = StreamListener()

tweet = []


class MyStream(tweepy.Stream):
    tweets = 0

    def on_data(self, data):
        print(dir(data))
        self.tweet_raw = data



stream = MyStream(os.getenv("CONSUMER_KEY"),
                        os.getenv("CONSUMER_SECRET"),
                        os.getenv("ACCESS_TOKEN"),
                        os.getenv("ACCESS_TOKEN_SECRET"))

# setup the stream, break it to look at the tweet_raw
stream.filter(track = names)
print(stream.tweet_raw)
#convert to dictionary
a= stream.tweet_raw
#last step convert to json, dont know how yet
dict = json.loads(a.decode('utf-8'))
dict["text"]
json.dumps(dict, indent = 4)