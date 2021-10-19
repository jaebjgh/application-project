import filter_stream
from filter_stream import bearer_oauth
import requests
import geopandas as gpd
import os
import json
from dotenv import load_dotenv

# Retrieve district names
plz_shape_df = gpd.read_file('../../OSM/Hamburg.geojson')
names = [district['name'] for district in plz_shape_df.tags]


def set_rules():
    # You can adjust the rules if needed
    # example rule : [{"value": "wandsbek lang:de", "tag": "wandsbek"}]
    sample_rules = [{'value': f"{name} lang:de", 'tag': f'{name}'} for name in names[:25]]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))


def get_stream():
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream", auth=bearer_oauth, stream=True,
    )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            print(json.dumps(json_response, indent=4, sort_keys=True))

filter_stream.delete_all_rules(filter_stream.get_rules())

set_rules()        
get_stream()

