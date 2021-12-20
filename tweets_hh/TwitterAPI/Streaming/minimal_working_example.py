import tweepy
stream = tweepy.Stream(Credentials)
stream.filter(track=['IB.SH'], languages = ['de'])