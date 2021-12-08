import pandas as pd
import numpy as np
import nltk
import re
import json
from datetime import datetime
from my_german_sentiment import MySentimentModel
import spacy
from spacy import displacy 
import matplotlib.pyplot as plt 
import numpy as np
from matplotlib.pyplot import figure
pd.set_option('display.max_colwidth', None)
model = MySentimentModel(model_name = "oliverguhr/german-sentiment-bert")

#########################################
# load collected tweets                 #
#########################################

df = pd.read_csv('streaming_tweets_29861.csv')
list_columns = ['_id', 'created_at', 'text', 'extended_tweet.full_text', 'user.friends_count', 'retweeted_status.source']
df[list_columns].sample(3)


#########################################
# filter retweets and train info        #
#########################################
print('total number of tweets: {}'.format(len(df)))
df = df[df['retweeted_status.source'].isna()]
print('total number of tweets without retweets: {}'.format(len(df)))
df = df[~df['user.name'].isin(['metronom4me', 
                               'metronom RE3 Hamburg Lüneburg Uelzen', 
                               'Metronom RE4 Hamburg Rotenburg Bremen',
                               'erixx.de', 
                               'eurobahn', 
                               'zuginfo.nrw',
                               'HADAG - Genau deine Elbe.',
                               'DB Regio Schleswig-Holstein'])]
print('total number of tweets without retweets and without train information: {}'.format(len(df)))
df['user.name'].value_counts()


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

df['full_text'] = df.apply(get_full_text, axis=1)
df = df.drop(columns=['text', 'extended_tweet.full_text'])
list_columns = ['_id', 'created_at', 'full_text', 'user.friends_count', 'retweeted_status.source']
df[list_columns].sample(5)


#########################################
# normalize document                    #
#########################################

#def normalize_document(doc):
#    """Normalize the document (lower case, stopword removal, ...)"""
#    stop_words = nltk.corpus.stopwords.words('german')
#    wpt = nltk.WordPunctTokenizer()
#    doc = re.sub('\S*@\S*\s?', '', doc)       # remove emails
#    doc = re.sub(r'http[\S]+', 'URL', doc)    # replace URLs
#    doc = re.sub(r'[^a-zA-Z\s\u00c4\u00e4\u00d6\u00f6\u00dc\u00fc\u00df]', '', doc)     # keep alphabet and spaces
#    doc = doc.lower()
#    doc = doc.strip()
#    tokens = wpt.tokenize(doc)
#    filtered_tokens = [token for token in tokens if token not in stop_words]
#    return filtered_tokens
#df['tokenized_tweet'] = df['full_text'].apply(normalize_document)


#########################################
# clean text                            #
#########################################

df['clean_text'] = df['full_text'].apply(model.clean_text)


#########################################
# column with matching district         #
#########################################

list_columns = ['_id', 'created_at', 'full_text', 'user.friends_count', 'district', 'user.name', 'user.description']

with open('match_dict.json', 'r') as fp:
    match_dict = json.load(fp)

#match_dict = {k.lower(): v for k,v in match_dict.items()}

def matching_district(doc):
    for key in match_dict.keys():
        if re.search(key, doc, re.IGNORECASE):
            return match_dict[key]


df['district'] = df['full_text'].apply(matching_district)
df = df[df['district'].notna()]
df[list_columns].sample(5)

#########################################
# detect if tweet contains 'hamburg'    #
#########################################
df['user.name'] = df['user.name'].astype(str)
df['user.description'] = df['user.description'].astype(str)
all_keywords = list(set(match_dict.keys()))
unique_keywords = [key for key in all_keywords if key not in ['Altstadt','Horn', 'Neustadt', 'Neuland', 'Hamm', 'Marienthal']]
unique_keywords.extend(['hamburg', 'hh'])
unique_keywords = [key.lower() for key in unique_keywords]

df['is_hamburg'] = [True if (any(x in text for x in unique_keywords) | ('hamburg' in (name+desc).lower())) else False for text, name, desc in zip( df['clean_text'], df['user.name'], df['user.description'])]

df['is_hamburg'].value_counts()
df_ham = df[df.is_hamburg]

#########################################
# detect if district is a place in tweet#
#########################################

nlp = spacy.load('de_core_news_sm')
# Text with nlp
is_loc = []
for text, district in zip(df_ham['clean_text'], df_ham['district']):
    doc = nlp(text)    
    # Display Entities
    list_loc = [(token.text) for token in doc if token.ent_type_ == 'LOC']
    loc_string = ' '.join([str(item) for item in list_loc])
    if re.search(district, loc_string, re.IGNORECASE):
        is_loc.append(True)
        #displacy.render(doc, style="ent")
    else:
        is_loc.append(False)
df_ham['district_is_loc'] = is_loc
list_columns.append('district_is_loc')
df_ham['district_is_loc'].value_counts()
df_loc = df_ham[df_ham['district_is_loc']]
df_loc[list_columns].sample(5)


#########################################
# number of tweets per district         #
#########################################

figure(figsize=(20, 10), dpi=80)
y = df_loc['district'].value_counts().index
x = df_loc['district'].value_counts().values
plt.semilogx()
plt.plot(x,y)


#########################################
# german sentiment analysis             #
#########################################

#df_loc = pd.read_csv('Streaming_Tweets_preproc.csv')
predictions = []
step_size = 100
for i in np.arange(0, len(df_loc), step_size):
    for prediction in model.predict_sentiment(list(df_loc.iloc[i:i+step_size]['clean_text'])):
        predictions.append(prediction)
    print('{}/{}'.format(len(predictions), len(df_loc)))
df_loc['sentiment'] = [sentiment[0] for sentiment in predictions]
df_loc['sentiment_score'] = [sentiment[1] for sentiment in predictions]
df_loc.to_csv('df_sent.csv')
df_loc[list_columns].sample(5)


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
df_loc['datetime'] = df_loc['created_at'].apply(to_datetime)
df_loc['datetime'] = pd.to_datetime(df_loc['datetime'])
df_loc[df_loc['datetime'].notna()].set_index('datetime').resample(rule='15T').count()['_id'].plot(figsize=(15,5), color = "#7482AA")