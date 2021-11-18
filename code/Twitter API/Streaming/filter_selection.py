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

# other, now not important anymore
# Retrieve district names
#plz_shape_df = gpd.read_file('../../OSM/Hamburg.geojson')
#names = [district['name'] for district in plz_shape_df.tags]
#places = gpd.read_file('../../Mapping/HH_WFS_Gruenflaechen.gml', driver ='GML')
#places_names = [place.lstrip() for name in places.name for place in name.split(',') if len(place) < 60]
#to_track = names + places_names

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

