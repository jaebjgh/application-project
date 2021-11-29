import folium
from shapely.geometry import Polygon
from shapely.ops import linemerge
import geopandas as gpd
from geopandas.geodataframe import GeoDataFrame
import pandas as pd

### Mapping Class
class Map:
    def __init__(self, geoms: GeoDataFrame):
        self.geom = geoms

    def draw(self):
        m = folium.Map(location=[53.551, 9.993], zoom_start=10, tiles="Stamen Toner")
        
        folium.GeoJson(self.geom, name="geometry", style_function=style_function, 
            highlight_function=highlight_function).add_to(m)
        return m

    def popup(self, text: str, location: str):
        pass
        

def style_function(feature):
    return {
        "opacity": 0.5,
        "weight": 0.5,
        "color": "#000000",
    }

def highlight_function(feature):
    return {
        "opacity": 0.5,
        "weight": 0.7,
        "color": "#FF1493",
    }



### LineStrings to Polygons
def make_polygons(geo_column):
    new_geo = []
    for row in geo_column:
        try: 
            merged = linemerge(row)
            new_geo.append(Polygon(merged))
        except:
            new_geo.append(Polygon([coords for geom in row for coords in geom.coords]))
    return new_geo

### 

"""
#Streets:
osm_Altona_streets = gpd.read_file('../OSM/Altona_streets.geojson')
streets = gpd.read_file('HH_WFS_Strassen_und_Wegenetz_gesamt', driver='GML')
altona_streets = streets[streets.gemeindeschluessel.isin(list(range(201,207)))].set_crs('ETRS89', allow_override= True)
double_streets = {row['properties']['strassenname'] for row in altona_streets.iterfeatures() if len(streets[(streets.strassenname == row['properties']['strassenname']) & ~(streets.gemeindeschluessel.isin(list(range(201,207))))]) > 1}
"""
if __name__ == "__main__":

    hamburg = gpd.read_file('../OSM/Hamburg.geojson')

    # Collection of LineStrings to Polygons: 
    hamburg["geometry"] = make_polygons(hamburg.geometry)

    mp = Map(hamburg)
    m = mp.draw()
    m

"""

Setting a marker in the middle of a district is fairly easy, 
but we cannot update the map on the go :( 
No option to remove markers / include new ones or the like. 

Marker for Neugraben-Fischbek:
folium.Marker([plz_shape_df.geometry.iloc[1].centroid.y, plz_shape_df.geometry.iloc[1].centroid.x]).add_to(m)
m
"""

##### Development
import random
if __name__ == "__main__":

    test_df = pd.read_json("../TwitterAPI/DemoTweets/demo_keywords_raw.json")
    sentiment = [0,1,2]
    test_df["sentiment"] = random.choices(sentiment, k = test_df.shape[0])