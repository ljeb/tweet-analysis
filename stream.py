import tweepy
import json
import operator
import time

import re
import config
from textblob import TextBlob
from tweepy.streaming import StreamListener
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import API
from collections import defaultdict


class MyListener(StreamListener):
    
    def __init__ (self, time_limit=300):
        self.start_time = time.time()
        self.limit = time_limit
        self.outFile = open("third.json", "w")
        super(MyListener, self).__init__()
        
    def on_data(self, data):
        if (time.time() - self.start_time) < self.limit:
            self.outFile.write(data)
            return True
        else: 
            self.outFile.close()
            return False
    
    def on_error(self, status):
        print(status)

def stream():

    C_KEY = config.C_KEY
    C_SECRET = config.C_SECRET
    A_TOKEN_KEY = config.A_TOKEN_KEY
    A_TOKEN_SECRET = config.A_TOKEN_SECRET

    auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
    auth.set_access_token(A_TOKEN_KEY, A_TOKEN_SECRET)
    api = tweepy.API(auth)


    myStream = Stream(auth, MyListener(time_limit=1200))
    myStream.filter(track=["bernie", "sanders", "@berniesanders", "elizabeth", "warren", "@ewarren", "joe", "biden", "@joebiden", "pete", "buttigieg", "@PeteButtigieg", "kamala", "harris", "@KamalaHarris", "andrew", "yang", "@AndrewYang", "cory", "booker", "@CoryBooker", "amy", "klobuchar", "@amyklobuchar", "tom", "steyer", "@TomSteyer", "tulsi", "gabbard", "@TulsiGabbard"])

stream()
