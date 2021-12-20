import random

import folium
from shapely.geometry import Polygon, Point
from shapely.ops import linemerge
from geopandas.geodataframe import GeoDataFrame
import pandas as pd

## Mapping Class
class Map:
    def __init__(self, geoms: GeoDataFrame, tweet_df: pd.DataFrame, population: pd.DataFrame):
        self.merged = pd.merge(geoms, tweet_df, left_on="name", right_on="district", how="left")
        tweet_stats = self.merged.groupby("name")["sentiment"]\
                              .agg(
                        share_positive=lambda value: round((value == "positive").sum() / value.count(), 4) * 100 if value.count() > 0 else 0 ,
                        share_negative = lambda value: round((value == "negative").sum() / value.count(), 4) * 100 if value.count() > 0 else 0, 
                        n_tweets=lambda value: value.count()
                                    ).reset_index()

        self.stats = pd.merge(geoms, tweet_stats, on = "name")

        self.base = folium.Map(location=[53.551, 9.993], zoom_start=10, tiles="Stamen Toner")

        self.pop = population

    def draw_map(self, on = None, hours: int = 24, exclude=None):
        self.m = self.base
        self.display_curr_tweets(on=on, hours_interval=hours)
        self.heatmap()
        self.tweets_per_pop(exclude)
        self.more_happy_than_not()
        folium.map.LayerControl().add_to(self.m)
        
        return self.m
        

    def display_curr_tweets(self, on, hours_interval):   
        # time filtering
        delta = pd.Timedelta(hours_interval, unit="H")
        if on:
            dot = pd.to_datetime(on, utc=True) 
        else:
            dot = self.merged.created_at.max().replace(hour=0, minute=0, second=0)
        till = dot + delta
        #start_date = self.merged.created_at.max()+delta
        plot_df = self.merged[(self.merged.created_at >= dot) & (self.merged.created_at <= till)]
        plot_df.geometry = [generate_random(poly) for poly in plot_df.geometry]
        
        if hours_interval == 24:
            dot = dot.date()
        else:  
            dot, till = map(lambda t: str(t).split('+')[0], (dot, till))
        title = f'Tweets ({dot})' if hours_interval == 24 else f'Tweets ({dot} - {till})'
        layer = folium.FeatureGroup(name=title, show=True, overlay=True)

        # iterate over GEOJSON features, pull out point coordinates, make Markers and add to layer
        for tweet in plot_df.iterrows():
            
            colors = {"positive": "green",
                     "neutral": "yellow",
                     "negative": "red"}
            props = tweet[1]
            fill_color = colors[props["sentiment"]]

            timestamp = props["created_at"]
            text = props["clean_text"]

            folium.Marker(location=(props["geometry"].y, props["geometry"].x),
                        icon=folium.Icon(
                            icon_color=fill_color,
                            icon='twitter',
                            prefix='fa'), 
                        popup = f"""
                        <p>{timestamp}<\p>
                        <p>{text}<\p>
                        """
                         
                        ).add_to(layer)

        layer.add_to(self.m)


    def heatmap(self, exclude=None):

        choropleth = folium.Choropleth(name = "Tweets per district",
            geo_data = self.stats,
            data=self.stats[self.stats.name != exclude] if exclude else self.stats,
            columns=['name', 'n_tweets'],
            key_on ="feature.properties.name",
            fill_opacity=1,
            legend_name='Tweets per district',
            fill_color="RdPu", overlay=True, show=False, highlight = True).add_to(self.m)

        style_function = "font-size: 15px; font-weight: bold"
        choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['name', 'n_tweets'], style=style_function, labels=True))


    def tweets_per_pop(self, exclude=None):
        to_plot = pd.merge(self.stats, self.pop, on="name")
        to_plot["tweets_per_resident"] = [to_plot["n_tweets"][idx] / pop if pop > 0 else 0 for idx, pop in enumerate(to_plot["population"])]
        
        self.heat_per_pop = self.base
        choropleth = folium.Choropleth(name = "Tweets per resident",
            geo_data =to_plot,
            data=to_plot[to_plot.name != exclude] if exclude else to_plot, # Neuwerk is an outlier with .33 
            columns=['name', 'tweets_per_resident'],
            key_on ="feature.properties.name",
            fill_opacity=1,
            legend_name='Tweets per resident',
            fill_color="RdPu", overlay=True, show = False, highlight = True).add_to(self.m)

        style_function = "font-size: 15px; font-weight: bold"
        choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['name', 'population', 'tweets_per_resident'], style=style_function, labels=True))

    def more_happy_than_not(self, exclude=None):
        to_plot = self.stats
        to_plot["pos2neg"] = [to_plot.share_positive[idx] / share_neg if share_neg != 0 else None for idx, share_neg in enumerate(to_plot["share_negative"])]
        self.positive = self.base
        choropleth = folium.Choropleth(name = "Ratio of positive to negative tweets",
            geo_data = to_plot[to_plot.name != exclude] if exclude else to_plot,
            data=to_plot,
            columns=['name', 'pos2neg'],
            key_on ="feature.properties.name",
            fill_opacity=1,
            nan_fill_color='grey',
            legend_name='Ratio of positive to negative tweets',
            fill_color="RdPu", overlay=True, show = False, highlight= True).add_to(self.m)

        style_function = "font-size: 15px; font-weight: bold"
        choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['name', 'pos2neg', 'n_tweets'], style=style_function, labels=True))


## All about polygons
def generate_random(polygon):
    minx, miny, maxx, maxy = polygon.bounds
    while True:
        pnt = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        if polygon.contains(pnt):
            return pnt


    # LineStrings to Polygons
def make_polygons(geo_column):
    new_geo = []
    for row in geo_column:
        try: 
            merged = linemerge(row)
            new_geo.append(Polygon(merged))
        except:
            new_geo.append(Polygon([coords for geom in row for coords in geom.coords]))
    return new_geo






