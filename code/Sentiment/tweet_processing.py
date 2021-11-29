import pandas as pd
import numpy as np
import nltk
import re
from datetime import datetime

df = pd.read_csv('../Twitter API/Streaming/streaming_tweets_16830.csv')
df.head()
list_columns = ['_id', 'created_at', 'text', 'extended_tweet.full_text', 'user.friends_count', 'retweeted_status.source']
df[list_columns].head()

def get_full_text(row):
    if isinstance(row['extended_tweet.full_text'], str):
        return row['extended_tweet.full_text']
    elif isinstance(row['text'], str):
        return row['text']
    else:
        return 'nan'

df['extended_tweet.full_text'] = df.apply(get_full_text, axis=1)
df[list_columns].head()

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

def clean_text(doc):
    doc = doc.replace("\n", " ")        
    doc = re.compile(r'@\\S+', re.MULTILINE).sub('',doc)        
    doc = re.compile(r'[^A-Za-züöäÖÜÄß ]', re.MULTILINE).sub('', doc) # use only text chars                          
    doc = ' '.join(doc.split()) # substitute multiple whitespace with single whitespace   
    doc = doc.strip().lower()
    return doc
df['clean_text'] = df['extended_tweet.full_text'].apply(clean_text)

from germansentiment import SentimentModel
model = SentimentModel()
#df['sentiment'] = 
model.predict_sentiment(list(df['clean_text'].head(100)))

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