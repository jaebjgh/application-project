import folium
import geopandas as gpd
from geopandas.geodataframe import GeoDataFrame

class Map:
    def __init__(self, geoms: GeoDataFrame):
        self.geom = geoms

    def draw(self):
        m = folium.Map(location=[53.551, 9.993], zoom_start=10, tiles="Stamen Toner")
        
        folium.GeoJson(self.geom, name="geometry", style_function = style_function,).add_to(m)
        return m

def style_function(feature):
    return {
        "opacity": 0.5,
        "weight": 0.5,
        "color": "#000000",
    }


"""
plz_shape_df = gpd.read_file('../OSM/Hamburg.geojson')

mp = Map(plz_shape_df)
m = mp.draw()

folium.Marker(list(plz_shape_df.geometry.iloc[0].centroid.coords)[0], color = "red").add_to(m)
m

"""