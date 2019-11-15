import tweepy
import json
import operator
import time

import re
from textblob import TextBlob
from tweepy.streaming import StreamListener
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import API
from collections import defaultdict

def get_tweets(file_name):
    f = open(file_name)
    tweets = [json.loads(line) for line in f]
    f.close()

    counts = defaultdict(int)
    tweets = [tweet['text'] for tweet in tweets]
    return tweets
    
def print_results(tweets):
    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if get_tweet_sentiment(tweet) == 'positive']
    # percentage of positive tweets
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if get_tweet_sentiment(tweet) == 'negative']
    # percentage of negative tweets
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
    # percentage of neutral tweets
    print("Neutral tweets percentage: {} %".format(100 - (100*len(ptweets)/len(tweets)) - (100*len(ntweets)/len(tweets))))

    # printing first 5 positive tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet)

    # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet)

def clean_tweet(tweet):
    '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def get_tweet_sentiment(tweet):
    '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
    # create TextBlob object of passed tweet text
    analysis = TextBlob(clean_tweet(tweet))
    # set sentiment
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

tweets = get_tweets("output.json")
print_results(tweets)

