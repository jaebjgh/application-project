import json
import requests

import geopandas as gpd

# Retrieve HH district boundaries from Overpass API
overpass_url = "http://overpass-api.de/api/interpreter"


overpass_query_districts = """
[out:json];
area["ISO3166-2"="DE-HH"];
rel["boundary"="administrative"]["admin_level"=10](area);
convert item ::=::,::geom=geom(),_osm_type=type();
out geom;
"""
#

op_q_streets_altona_alt = """
[out:json];
area(3600077384);
(
way(area)
['name']
['highway']
['highway' !~ 'motorway']
['highway' !~ 'motorway_link']
['highway' !~ 'raceway']
['highway' !~ 'proposed']
['highway' !~ 'construction']
['highway' !~ 'elevator']
['highway' !~ 'bus_guideway']
['foot' !~ 'no']
['access' !~ 'private']
['access' !~ 'no'];
);
convert item ::=::,::geom=geom(),_osm_type=type();
out geom;

"""


response = requests.get(overpass_url, 
                        params={'data': overpass_query_districts})

"""
---Interlude---
>>convert item ::=::,::geom=geom(),_osm_type=type();<< is for 'geojson' 
--> without the output would be plain json 

But you think you're done? No way, José :') This is still no valid geojson.
Valid geojson has to look like this: https://datatracker.ietf.org/doc/html/rfc7946#section-1

"""
# Converting to valid geojson format
response_data = response.json()['elements']

out = {"type": "FeatureCollection",
  "features": []}

for feature in response_data:
    feature["type"] = 'Feature'
    feature["name"] = feature["tags"]["name"]
    out["features"].append(feature)

# Save geojson file
with open('Altona_streets.geojson', 'w') as geojson:
    json.dump(out, geojson)

# Read in geojson file and plot
plz_shape_df = gpd.read_file('Altona_streets.geojson')
plz_shape_df.plot() # ugly indeed but Hamburg is recognizable 


