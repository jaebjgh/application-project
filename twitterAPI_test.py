#######################
# Packages ############
#######################

import tweepy
import os
import pandas as pd
import pymongo

from dotenv import load_dotenv

#######################
# Authentication ######
#######################

# Load variables found in .env as environment variables
dirname = os.getcwd()
envfile = os.path.join(dirname, '.env')
load_dotenv(envfile)

auth = tweepy.OAuthHandler(os.getenv("CONSUMER_KEY"),
                           os.getenv("CONSUMER_SECRET"))  # app
auth.set_access_token(os.getenv("ACCESS_TOKEN"),
                      os.getenv("ACCESS_TOKEN_SECRET"))  # user
api = tweepy.API(auth)

tweepy_client = tweepy.Client(bearer_token=os.getenv("BEARER_TOKEN"), 
                       consumer_key=os.getenv("CONSUMER_KEY"), 
                       consumer_secret=os.getenv("CONSUMER_SECRET"),
                       access_token=os.getenv("ACCESS_TOKEN"),
                       access_token_secret=os.getenv("ACCESS_TOKEN_SECRET"))


#################
# API Endpoints #
#################

# 1. User timeline
user_timeline = api.user_timeline()
status = user_timeline[0]
status._json
status.text
status.entities

# 2. Send and delete a tweet
api.update_status("First Tweet")
user_timeline = api.user_timeline()
len(user_timeline)
last_status = user_timeline[0].text
last_status_id = user_timeline[0].id
api.destroy_status(last_status_id)

# 3. User data
user = api.get_user(screen_name = "lillz_lillian")       # Other user
user._json
user.name
user.screen_name
user.followers_count

# 4. Home timeline
home_timeline = api.home_timeline()
len(home_timeline)         # 20 Statuses
type(home_timeline)        # tweepy.models.ResultSet
type(home_timeline[0])     # tweepy.models.Status
home_timeline[1]._json

# 5. Search
tweets = api.search_tweets(q='#ampel -filter:retweets -filter:replies',
                    result_type="recent",  # mixed/recent/popular
                    count=20,
                    tweet_mode='extended')

############################
# Tesla Data #
############################
user = api.get_user(screen_name = "tesla")       # Other user
print(f"Number of followers : {user.followers_count}")
print(f"Number of friends : {user.friends_count}")
print(f"Number of tweets : {user.statuses_count}")

tesla_timeline = api.user_timeline(screen_name = 'tesla', count = 20, exclude_replies = True)
print(f"Text of last tweet: {tesla_timeline[0].text}")
print(f"Number of favorites on that tweet : {tesla_timeline[0].favorite_count}")
print(f"Number of retweets : {tesla_timeline[0].retweet_count}")
number_replies = client.get_tweet(id = tesla_timeline[0].id, 
                 tweet_fields=["public_metrics"]).data.public_metrics['reply_count']
print(f"Number of replies : {number_replies}")

################################
# 300 tweets with #datascience #
################################
datascience_tweets =tweepy.Cursor(api.search_tweets, q='#datascience -filter:retweets -filter:replies',
                    result_type="recent",  # mixed/recent/popular
                    count = 100, 
                    tweet_mode='extended').items(1000)

datascience_tweets = [item for item in datascience_tweets]
print(len(datascience_tweets))

### Save in MongoDB
client = pymongo.MongoClient('localhost:27017')
db = client["sma"]
collection = db['datascience']

for tweet in datascience_tweets:
    tweet_json = tweet._json
    tweet_json['_id'] = tweet_json.pop('id')  # change name of tweet id so no duplicate tweet is stored
    try:
        collection.insert_one(tweet_json)
    except pymongo.errors.DuplicateKeyError:
        continue

# Get Tweets back from MongoDB
documents = [i for i in collection.find()]
df = pd.DataFrame(documents)

# Only tweets in german language
# with filter select value that has to meet criteria
# with projection select values with list that have to be returned
collection.find(filter = {'lang': 'de', 'possibly_sensitive' : False}, projection = ['full_text', 'lang'])[0]

################################
# searching for wandsbek #
################################

client = pymongo.MongoClient('localhost:27017')
db = client["sma"]
collection = db['wandsbek']
wandsbek_search =tweepy.Paginator(tweepy_client.search_recent_tweets, query='#wandsbek', 
                             max_results = 10).flatten(limit=10)
wandsbek_tweets = [item for item in wandsbek_search]
wandsbek_tweets

print(len(wandsbek_tweets))
for tweet in wandsbek_tweets:
    try:
        collection.insert_one(wandsbek_search)
    except pymongo.errors.DuplicateKeyError:
        continue

############################
# Processing option #
############################

# Print results
for tweet in tweets:
    print(f"{tweet.user.name} said: {tweet.full_text} \n---")


# Save in Pandas DataFrame
json_data = [tweet._json for tweet in tweets]
df = pd.json_normalize(json_data)

### Save in MongoDB
client = pymongo.MongoClient('localhost:27017')
db = client["sma"]
collection = db['tesla']

for tweet in tweets:
    try:
        collection.insert_one(tweet._json)
    except pymongo.errors.DuplicateKeyError:
        continue

# Query from MongoDB
collection.count_documents({})
collection.find()[0]
documents = [i for i in collection.find()]
df = pd.DataFrame(documents)
df_flat = pd.json_normalize(documents)


##############
# Paginating #
##############
# .. through items
home_timeline = tweepy.Cursor(api.home_timeline).items(10)
[item.created_at for item in home_timeline]


# ... through pages
home_timeline = tweepy.Cursor(api.home_timeline).pages(2)
[item.created_at for page in home_timeline for item in page]

client = pymongo.MongoClient('localhost:27017')
db = client["twitter"]
collection = db['datascience']
res = collection.find({}, {'user'})
[i for i in res]
