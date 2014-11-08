#!/usr/bin/python 
from twitter import *

auth = OAuth(
    consumer_key='gKaAE8q1gtSiKxxsTBZUA',
    consumer_secret='zvLMiCy1Lx49OsBGksAVLPYfXBEn2iASvHSJGXtw8',
    token='19982211-kCJThkO6AWRO6yGQkO00b3rqGUg44Zr35RHTacRB4',
    token_secret='nTAhC1Wb9QoZM28NGcbrbfdunuPlnWM0Nk8bDaG0zKw'
)

stream = TwitterStream(auth = auth, secure = True)
tweet_iter = stream.statuses.filter(track = "love")

for tweet in tweet_iter:
    # check whether this is a valid tweet
    if tweet.get('text'):
        # yes it is! print out the contents, and any URLs found inside
        print "(%s) @%s %s" % (tweet["created_at"], tweet["user"]["screen_name"], tweet["text"])


