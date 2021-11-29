import os
import json
import pymongo
import pandas as pd 
import tweepy
from dotenv import load_dotenv
import geopandas as gpd
import sys

sys.path.append("../../Mapping/")
from mapping import make_polygons

# Retrieve district names
plz_shape_df = gpd.read_file('../../OSM/Hamburg.geojson')
names = [district['name'] for district in plz_shape_df.tags]
places = gpd.read_file('../../Mapping/HH_WFS_Gruenflaechen.gml', driver ='GML')
places_names = [place.lstrip() for name in places.name for place in name.split(',') if len(place) < 60]
to_track = names + places_names

# Match keywords and districts
match_dict = {}
for name in names:
    match_dict[name] = name

plz_shape_df["geometry"] = make_polygons(plz_shape_df.geometry)

match_dict["Emil-Wendt-Park"] = "Altona-Altstadt"
match_dict["Baakenpark"] = "HafenCity"
match_dict["Suttnerpark"] = "Altona-Altstadt"
match_dict["Außenalster"] = "Rotherbaum"
match_dict["Hirschpark"] = "Nienstedten"
match_dict["Große Moorweide"] = "Rotherbaum"
match_dict["Trauns Park"] = "Rothenburgsort"
match_dict["Alter Elbpark"] = "Neustadt"
match_dict["Alter Friedhof Harburg"] = "Harburg"
match_dict["Alsterpark"] = "Fuhlsbüttel"
match_dict["Amsinckpark"] = "Lokstedt"
match_dict["August-Lütgens-Park"] = "Altona-Altstadt"
match_dict["BallinPark"] = "Wilhelmsburg"
match_dict["Baurs Park"] = "Blankenese"
match_dict["BallinPark"] = "Wilhelmsburg"
match_dict["Bergedorfer Schlossgarten"] = "Bergedorf"
match_dict["Berner Gutspark"] = "Farmsen-Berne"
match_dict["Blohms Park"] = "Horn"
match_dict["Bolivarpark"] = "Winterhude"
match_dict["Bonne Park"] = "Bahrenfeld"
match_dict["Donners Park"] = "Ottensen"
match_dict["Eichenpark"] = "Harvestehude"
match_dict["Eichtalpark"] = "Wandsbek"
match_dict["Elbpark Entenwerder"] = "Rothenburgsort"
match_dict["Luusbarg"] = "Rissen"
match_dict["Goßlers  Park"] = "Blankenese"
match_dict["Grünzug Göhlbachtal"] = "Eißendorf"
match_dict["Hammer Park"] = "Hamm"
match_dict["Hayns Park"] = "Eppendorf"
match_dict["Hennebergpark"] = "Poppenbüttel"
match_dict["Hessepark"] = "Blankenese"
match_dict["Altonaer Balkon"] = "Altona-Altstadt"
match_dict["Innocentiapark"] = "Harvestehude"
match_dict["Jugendpark Langenhorn"] = "Langenhorn"
match_dict["Kellinghusen Park"] = "Eppendorf"
match_dict["Liliencronpark"] = "Rahlstedt"
match_dict["Drachenthalpark / Parkanlage Neuwiedenthal"] = "Hausbruch"
match_dict["Lohmühlengrünzug"] = "St. Georg"
match_dict["Lutherpark"] = "bahrenfeld"
match_dict["Fischers Park"] = "Ottensen"
match_dict["Ohlendorffs Park"] = "Volksdorf"
match_dict["Parkanlage Grindelberg"] = "Harvestehude"
match_dict["Planten un Blomen"] = "St. Pauli"
match_dict["Platz der Republik"] = "Altona-Altstadt"
match_dict["Pulverhofpark"] = "Rahlstedt"
match_dict["Rathauspark Bergedorf"] = "Bergedorf"
match_dict["Rathenaupark"] = "Ottensen"
match_dict["Römischer Garten"] = "Blankenese"
match_dict["Rüschpark"] = "Finkenwerder"
match_dict["Schillerufer"] = "Bergedorf"
match_dict["Schinckels Park"] = "Blankenese"
match_dict["Schleepark"] = "Altona-Altstadt"
match_dict["Seelemannpark"] = "Eppendorf"
match_dict["Sola Bona Park"] = "Eidelstedt"
match_dict["Glockenhausgarten"] = "Billwerder"
match_dict["Antonipark"] = "Altona-Altstadt"
match_dict["Sternschanzenpark"] = "Sternschanze"
match_dict["Sven Simon Park"] = "Blankenese"
match_dict["Biedermannplatz"] = "Barmbek-Süd"
match_dict["Botanischer Sondergarten Wandsbek"] = "Wandsbek"
match_dict["Eimsbütteler Park"] = "Eimsbüttel"
match_dict["Eppendorfer Park"] = "Eppendorf"
match_dict["Hans-Christian-Andersen-Park"] = "Osdorf"
match_dict["Heinepark"] = "Ottensen"
match_dict["Jacobipark"] = "Eilbek"
match_dict["Lise-Meitner-Park"] = "Bahrenfeld"
match_dict["Loki Schmidt Garten"] = "Klein Flottbek"
match_dict["Meyers Park Heinrich"] = "Heimfeld"
match_dict["Gorch-Fock-Park"] = "Finkenwerder"
match_dict["Rosengarten"] = "Harburg"
match_dict["Schröders Elbpark"] = "Othmarschen"
match_dict["Teetzpark"] = "Wandsbek"
match_dict["Thörls Park"] = "Hamm"
match_dict["Unnapark"] = "Eimsbüttel"
match_dict["Von-Eicken-Park"] = "Eimsbüttel"
match_dict["Wacholderpark"] = "Fuhlsbüttel"
match_dict["Waldpark Falkenstein"] = "Blankenese"
match_dict["Waldpark Steinfurth"] ="Billstedt"
match_dict["Große Moorweide "] = "Eimsbüttel"
match_dict["Wandsbeker Gehölz"] = "Wandsbek"
match_dict["Wasserpark Dove Elbe"] = "Bergedorf"
match_dict["Wehbers Park"] = "Eimsbüttel"
match_dict["Wesselhoeftpark"] = "Altona"
match_dict["Wohlerspark"] = "Altona"
match_dict["Appelhoffweiher"] = "Steilshoop"
match_dict["Bornpark"] ="Osdorf"
match_dict["Böverstpark"] ="Lurup"
match_dict["Falkensteiner Ufer Elbpark"] = "Blankenese"
match_dict["Friedhof Lohbrügge"] = "Bergedorf"
match_dict["Alsenpark"] ="Altona"
match_dict["Greifenbergpark"] = "Rahlstedt"
match_dict["Altonaer Volkspark"] = "Altona"
match_dict["Grothpark"] = "Othmarschen"
match_dict["Grünanlage am Sandberg"] = "Altona"
match_dict["Grünanlage am Willersweg"] = "Langenhorn"
match_dict["Grünes Zentrum Lohbrügge"] = "Bergedorf"
match_dict["Grünzug Langenfort"] = "Barmbek-Nord"
match_dict["Harburger Schlossinsel"] = "Harburg"
match_dict["Hauptfriedhof Altona"] = "Altona"
match_dict["Hohenhorstpark"] = "Wandsbek"
match_dict["Jenfelder Moorpark"] ="Jenfeld"
match_dict["Johannes Prassek Park"] = "Barmbek-Süd"
match_dict["Othmarschen Park"] ="Othmarschen"
match_dict["Parkanlage Langenbeker Feld"] = "Langenbek"
match_dict["Saseler Park"] ="Wandsbek"
match_dict["Schwarzenberg"] ="Harburg"
match_dict["Waldpark Marienhöhe"] = "Altona"
match_dict["Parkanlage am Neuländer See"] = "Harburg"
match_dict["Hohenbuchenpark"] = "Poppenbüttel"
match_dict["Öjendorfer Park"] = "Billstedt"
match_dict["Mühlenteichpark"] ="Wandsbek"
match_dict["Wilhelmsburger Inselpark"] = "Wilhelmsburg"
match_dict["Grasbrookpark"] = "Kleiner Grasbrook"
match_dict["Gustav-Mahler-Park"] = "Neustadt"
match_dict["Lohsepark"] = "HafenCity"
match_dict["Reiherstiegknie"] = "Wilhelmsburg"
match_dict["Sandtorpark"] = "Mitte"
match_dict["Bert-Kaempfert Platz"] = "Barmbek"
match_dict["Harburger Rathausplatz"] = "Harburg"
match_dict["Jarreplatz"] ="Winterhude"
match_dict["Kalischer Platz"] ="Harburg"
match_dict["Kanalplatz"] = "Harburg"
match_dict["Lohseplatz"] = "HafenCity"
match_dict["Löschplatz"] = "Barmbek-Nord"
match_dict["Lotsekai"] ="Harburg"
match_dict["Marie-Jonas-Platz"] ="Eppendorf"
match_dict["Marktplatz Sand"] = "Harburg"
match_dict["Schwanenwik"] = "Uhlenhorst"
match_dict["Straßburger Platz"] = "Dulsberg"
match_dict["Vorplatz Museum der Arbeit"] = "Barmbek-Nord"
match_dict["Winterhuder Marktplatz"] ="Winterhude"
match_dict["City-Nord-Park"] = "Winterhude"
match_dict["Harburger Stadtpark"] = "Harburg"
match_dict["Stadtpark Winterhude"] = "Winterhude"
match_dict["Jenischpark"] = "Othmarschen"
match_dict["Westerpark"] = "Nienstedten"
match_dict["Kapitän Schröder Park"] = "Altona"
match_dict["Park Mitte Altona"] = "Altona"
















































district_of_place1 = ["Altona-Altstadt", "HafenCity", "Altona-Altstadt",
                    "Rotherbaum"]
district_of_place2 = []
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