#######################
# Packages ############
#######################

import tweepy
import pytumblr
import os
import pandas as pd
import pymongo

from dotenv import load_dotenv
# Load variables found in .env as environment variables
dirname = os.getcwd()
envfile = os.path.join(dirname, '.env')
load_dotenv(envfile)

#######################
# Authentication ######
#######################

tumb_client = pytumblr.TumblrRestClient(
    os.getenv("CONSUMER_KEY_TUMBLR"),
    os.getenv("CONSUMER_SECRET_TUMBLR"),
    os.getenv("ACCESS_TOKEN_TUMBLR"),
    os.getenv("ACCESS_TOKEN_SECRET_TUMBLR"),
)

tumb_client.info() # Grabs the current user information


###########################
# read posts with wandsbek#
# and store inside MongoDB#
###########################
collection_tag = 'billstedt'
tagged_return = tumb_client.tagged(collection_tag)
tumblr_posts = [item for item in tagged_return]
client = pymongo.MongoClient('localhost:27017')
db = client["sma"]
collection = db[collection_tag]

for post in tumblr_posts:
    id_post = post
    id_post['_id'] = id_post.pop('id')
    try:
        collection.insert_one(post)
    except pymongo.errors.DuplicateKeyError:
        continue

collection.count_documents({})
for post in collection.find():
    print(post)