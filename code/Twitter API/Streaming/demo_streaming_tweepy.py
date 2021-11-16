import os
import json
import pymongo
import pandas as pd 
import tweepy
from dotenv import load_dotenv
import geopandas as gpd

# Retrieve district names
plz_shape_df = gpd.read_file('../../OSM/Hamburg.geojson')
names = [district['name'] for district in plz_shape_df.tags]
places = gpd.read_file('../../Mapping/HH_WFS_Gruenflaechen.gml', driver ='GML')
places_names = [place.lstrip() for name in places.name for place in name.split(',') if len(place) < 60]
to_track = names + places_names

# excluded Altstadt & Neustadt for demonstrative purposes 
#osm_Altona_streets = gpd.read_file('../../OSM/Altona_streets.geojson')
#streets = gpd.read_file('../../Mapping/HH_WFS_Strassen_und_Wegenetz_gesamt', driver='GML')
#altona_streets = streets[streets.gemeindeschluessel.isin(list(range(201,207)))].set_crs('ETRS89', allow_override= True)
#double_streets = {row['properties']['strassenname'] for row in altona_streets.iterfeatures() if len(streets[(streets.strassenname == row['properties']['strassenname']) & ~(streets.gemeindeschluessel.isin(list(range(201,207))))]) > 1}
#parks = gpd.read_file('../../Mapping/HH_WFS_Gruenplan.gml', driver='GML')
#parks[parks.verwaltungsvermoegen == "Flächen des Bezirks - Stadtgrün"].sort_values("flaeche_ha", ascending = False).head()
#parks.drop("geometry", axis = 1)['nutz_code'].value_counts()
#parks.to_csv("gruenplan.csv")


# Twitter restricts tracked phrases to 60 bytes
#altona_street_names = {name for name in altona_streets.strassenname if len(name) < 60}
#altona_parks = set(parks[(parks.ortsteil.isin(list(range(201,207)))) & (parks.benennung is not None)].benennung)
#phrases = {"Altona-Altstadt", "Altona Altstadt"}


#to_track = altona_street_names.union(altona_parks).union(phrases)
# Set up twitter API
load_dotenv('../../.env') # .env file in 'code' dir

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

#setup stream authentication
stream = MyStream(os.getenv("CONSUMER_KEY"),
                        os.getenv("CONSUMER_SECRET"),
                        os.getenv("ACCESS_TOKEN"),
                        os.getenv("ACCESS_TOKEN_SECRET"))

# setup the stream, break it to look at the tweet_raw
stream.filter(track=list(to_track), languages = ['de'])
#locations=[10.6444, 53.3960, 9.5663, 53.7516]