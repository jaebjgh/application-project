import numpy as np
import requests
import os

from dotenv import load_dotenv

# Load variables found in .env as environment variables
dirname = os.getcwd()
envfile = os.path.join(dirname, '.env')
load_dotenv(envfile)


##########################
# Using the yelp business search API: https://www.yelp.com/developers/documentation/v3/business_search

# headers contain the api key.
headers = {'Authorization': 'Bearer {}'.format(os.getenv("API_KEY"))}
search_api_url = 'https://api.yelp.com/v3/businesses/search'
params = {'term': 'coffee', 
          'location': 'Hamburg, Germany',
          'limit': 50}

# timeout of 5 seconds: https://requests.readthedocs.io/en/master/user/quickstart/#timeouts
response = requests.get(search_api_url, headers=headers, params=params, timeout=5)
id = response.json()['businesses'][0]['id']

# get reviews of one business
search_reviews_url = f'https://api.yelp.com/v3/businesses/{id}/reviews'
search_reviews_url
response = requests.get(search_reviews_url, headers=headers, params = {'locale' : 'de_DE'}, timeout=5)
response.json()['reviews'][0]['rating']