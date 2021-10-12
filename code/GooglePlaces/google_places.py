import requests
import os
import json

from dotenv import load_dotenv

## Get API key (saved it keys.env file)
load_dotenv(".env")
api_key = os.getenv("GOOGLE_API_KEY")

## example PlaceSearch (TextSearch): Restaurants in Altona
place_search = requests.get(f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=Altona&type=restaurant&key={api_key}")
search_results = place_search.json()['results']

## get a place id for adjacent PlaceDetails request
example_place_id = search_results[0]['place_id']

## PlaceDetails request
place_details = requests.get(f"https://maps.googleapis.com/maps/api/place/details/json?key={api_key}&fields=rating%2Creview%2Cuser_ratings_total&place_id={example_place_id}")
details_result = place_details.json()['result']
rating = details_result['rating'] #4.8
reviews = details_result['reviews'] # list of dictionaries (keys: author_name, author_url, language, rating, text, time, etc.)
user_ratings_count = details_result['user_ratings_total'] # 158

## save json for demonstrating purposes
with open('place_search.json', 'w') as placesearch_f:
    json.dump(place_search.json(), placesearch_f)

with open('place_details.json', 'w') as placedetails_f:
    json.dump(place_details.json(), placedetails_f)

