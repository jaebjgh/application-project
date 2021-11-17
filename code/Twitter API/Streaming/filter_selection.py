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
df = pd.DataFrame(to_track)
df.to_csv('names_to_track.csv')