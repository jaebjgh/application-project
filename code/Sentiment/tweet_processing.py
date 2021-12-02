import pandas as pd
import numpy as np
import nltk
import re
import json
from datetime import datetime
pd.set_option('display.max_colwidth', None)
#########################################
# load collected tweets                 #
#########################################

df = pd.read_csv('streaming_tweets_21113.csv')
list_columns = ['_id', 'created_at', 'text', 'extended_tweet.full_text', 'user.friends_count', 'retweeted_status.source']
df[list_columns].sample(3)

#########################################
# filter retweets                       #
#########################################

df = df[df['retweeted_status.source'].isna()]

#########################################
# set extended tweet as text            #
#########################################
def get_full_text(row):
    if isinstance(row['extended_tweet.full_text'], str):
        return row['extended_tweet.full_text']
    elif isinstance(row['text'], str):
        return row['text']
    else:
        return 'nan'

df['extended_tweet.full_text'] = df.apply(get_full_text, axis=1)
df[list_columns].sample(5)

#########################################
# normalize document                    #
#########################################

def normalize_document(doc):
    """Normalize the document (lower case, stopword removal, ...)"""
    stop_words = nltk.corpus.stopwords.words('german')
    wpt = nltk.WordPunctTokenizer()
    doc = re.sub('\S*@\S*\s?', '', doc)       # remove emails
    doc = re.sub(r'http[\S]+', 'URL', doc)    # replace URLs
    doc = re.sub(r'[^a-zA-Z\s\u00c4\u00e4\u00d6\u00f6\u00dc\u00fc\u00df]', '', doc)     # keep alphabet and spaces
    doc = doc.lower()
    doc = doc.strip()
    tokens = wpt.tokenize(doc)
    filtered_tokens = [token for token in tokens if token not in stop_words]
    return filtered_tokens
df['tokenized_tweet'] = df['extended_tweet.full_text'].apply(normalize_document)

#########################################
# clean text                            #
#########################################

def clean_text(doc):
    doc = doc.replace("\n", " ")        
    doc = re.compile(r'@\\S+', re.MULTILINE).sub('',doc)        
    doc = re.compile(r'[^A-Za-züöäÖÜÄß0-9,. ]', re.MULTILINE).sub('', doc) # use only text chars                          
    doc = ' '.join(doc.split()) # substitute multiple whitespace with single whitespace   
    #doc = doc.strip().lower()
    return doc
df['clean_text'] = df['extended_tweet.full_text'].apply(clean_text)

#########################################
# column with matching district         #
#########################################

list_columns.append('district')
list_columns.remove('retweeted_status.source')
import re
with open('match_dict.json', 'r') as fp:
    match_dict = json.load(fp)

match_dict = {k.lower(): v for k,v in match_dict.items()}

def matching_district(doc):
    for key in match_dict.keys():
        if re.search(key, doc, re.IGNORECASE):
            return match_dict[key]


df['district'] = df['extended_tweet.full_text'].apply(matching_district)
df = df[df['district'].notna()]
df[list_columns].sample(5)

#########################################
# detect if district is a place in tweet#
#########################################

import spacy
from spacy import displacy 
nlp = spacy.load('de_core_news_sm')
# Text with nlp
is_loc = []
for text, district in zip(df['clean_text'], df['district']):
    doc = nlp(text)    
    # Display Entities
    list_loc = [(token.text) for token in doc if token.ent_type_ == 'LOC']
    loc_string = ' '.join([str(item) for item in list_loc])
    if re.search(district, loc_string, re.IGNORECASE):
        is_loc.append(True)
        displacy.render(doc, style="ent")
    #       
    #
    #if district in list_loc:
    #    is_loc.append(True)
    #    displacy.render(doc, style="ent")
    else:
        is_loc.append(False)
df.drop(columns=['district_is_loc'])
df['district_is_loc'] = is_loc
list_columns.append('district_is_loc')
df['district_is_loc'].value_counts()
df_loc = df[df['district_is_loc']]
df_loc[list_columns].sample(20)



#########################################
# number of tweets per district         #
#########################################

import matplotlib.pyplot as plt 
import numpy as np
from matplotlib.pyplot import figure
figure(figsize=(20, 10), dpi=80)
y = df_loc['district'].value_counts().index
x = df_loc['district'].value_counts().values
plt.semilogx()
plt.plot(x,y)

#########################################
# german sentiment analysis             #
#########################################

import pandas as pd
df_loc = pd.read_csv('Streaming_Tweets_preproc.csv')
from my_german_sentiment import MySentimentModel
predictions = []
model = MySentimentModel(model_name = "oliverguhr/german-sentiment-bert")
step_size = 100
for i in np.arange(0, len(df_loc), step_size):
    for prediction in model.predict_sentiment(list(df_loc.iloc[i:i+step_size]['clean_text'])):
        predictions.append(prediction)
    print(i)
df_loc['sentiment'] = predictions
df_loc.to_csv('df_sent.csv')
#########################################
# set "created at" as datetime          #
#########################################

def to_datetime(timestamp):
    # dtime = tweet['created_at']
    try:
        new_datetime = datetime.strftime(datetime.strptime(timestamp,'%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S')
    except:
        new_datetime = np.nan
    return((new_datetime))

IBSH_colors = ['#7482AA', '#003064']
df['datetime'] = df['created_at'].apply(to_datetime)
df['datetime'] = pd.to_datetime(df['datetime'])
df[df['datetime'].notna()].set_index('datetime').resample(rule='15T').count()['_id'].plot(figsize=(15,5), color = "#7482AA")

df_loc.to_csv('Streaming_Tweets_preproc.csv')