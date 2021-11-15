import folium
import shapely
import geopandas as gpd
from geopandas.geodataframe import GeoDataFrame

class Map:
    def __init__(self, geoms: GeoDataFrame):
        self.geom = geoms

    def draw(self):
        m = folium.Map(location=[53.551, 9.993], zoom_start=10, tiles="Stamen Toner")
        
        folium.GeoJson(self.geom, name="geometry").add_to(m)
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

## Data
osm_Altona_streets = gpd.read_file('../OSM/Altona_streets.geojson')
streets = gpd.read_file('HH_WFS_Strassen_und_Wegenetz_gesamt', driver='GML')
altona_streets = streets[streets.gemeindeschluessel.isin(list(range(201,207)))].set_crs('ETRS89', allow_override= True)
double_streets = {row['properties']['strassenname'] for row in altona_streets.iterfeatures() if len(streets[(streets.strassenname == row['properties']['strassenname']) & ~(streets.gemeindeschluessel.isin(list(range(201,207))))]) > 1}
parks = gpd.read_file('HH_WFS_Gruenplan', driver='GML')

"""
# Collection of LineStrings to Polygons: 
plz_shape_df["geometry"] = [shapely.geometry.Polygon([coords for geom in row for coords in geom.coords]) for row in plz_shape_df["geometry"]]
"""

mp = Map(osm_Altona_streets)
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
