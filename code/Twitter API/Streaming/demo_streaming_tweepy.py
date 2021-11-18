import os
import json
import pymongo
import pandas as pd 
import tweepy
from dotenv import load_dotenv
import geopandas as gpd

#to_track = altona_street_names.union(altona_parks).union(phrases)
# Set up twitter API
load_dotenv('../../.env') # .env file in 'code' dir
to_track = pd.read_csv('names_to_track.csv')['0'].tolist()

# Set up MongoDB
client = pymongo.MongoClient('localhost:27017')
db = client["webgefluester"]
collection = db['streaming_tweets']

# inherit from tweepy.Stream class to change the on_data function
class MyStream(tweepy.Stream):

    #this function gets called when a tweet meets the search criteria
    def on_data(self, data):
        tweet = json.loads(data.decode('utf-8'))
        tweet['_id'] = tweet['id']
        collection.insert_one(tweet)

        print(tweet["created_at"]+":", tweet["text"], "\n", "-----")
        #self.tweet_raw = data



# function to start the stream with exeptions 

def start_stream():
    while True:
        try:
            #setup stream authentication
            stream = MyStream(os.getenv("CONSUMER_KEY"),
                        os.getenv("CONSUMER_SECRET"),
                        os.getenv("ACCESS_TOKEN"),
                        os.getenv("ACCESS_TOKEN_SECRET"))
            stream.filter(track=list(to_track), languages = ['de'])
        except KeyboardInterrupt: 
            break
        except:
            continue

start_stream()
#locations=[10.6444, 53.3960, 9.5663, 53.7516]
