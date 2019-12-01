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

candidates = {'andrewYang': ['andrew', 'yang', '@andrewyang'],
              'amyKlobuchar': ['amy', 'klobuchar', '@amyklobuchar'], 
              'bernieSanders': ['bernie', 'sanders', '@berniesanders'],
              'coryBooker': ['cory', 'booker', '@corybooker'],
              'elizabethWarren': ['elizabeth', 'warren', '@ewarren'], 
              'joeBiden': ['joe', 'biden', '@joebiden'], 
              'kamalaHarris': ['kamala', 'harris', '@kamalaharris'], 
              'peteButtigieg': ['pete', 'buttigieg', '@petebuttigieg'], 
              'tomSteyer': ['tom', 'steyer', '@tomsteyer'], 
              'tulsiGabbard': ['tulsi', 'gabbard', '@tulsigabbard']}

validLocations = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY",
          "Alabama","Alaska","Arizona","Arkansas","California","Colorado",
          "Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
          "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
          "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
          "Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York",
          "North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
          "Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
          "Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming", 
          "U.S.A", 'United States',]

def get_tweets(file_name):
    f = open(file_name)
    tweets = [json.loads(line) for line in f]
    f.close()
    
    tweets = [tweet['text'] for tweet in tweets if 'text' in list(tweet.keys())
              and 'retweeted_status' not in tweet and tweet['user']['location']
              and any(loc in tweet['user']['location'] for loc in validLocations)]
    
    return tweets
    
def results(tweets):
    ayt = [tweet for tweet in tweets if any(name in tweet.lower() for name in candidates['andrewYang'])]
    akt = [tweet for tweet in tweets if any(name in tweet.lower() for name in candidates['amyKlobuchar'])]
    bst = [tweet for tweet in tweets if any(name in tweet.lower() for name in candidates['bernieSanders'])]
    cbt = [tweet for tweet in tweets if any(name in tweet.lower() for name in candidates['coryBooker'])]
    ewt = [tweet for tweet in tweets if any(name in tweet.lower() for name in candidates['elizabethWarren'])]
    jbt = [tweet for tweet in tweets if any(name in tweet.lower() for name in candidates['joeBiden'])]
    kht = [tweet for tweet in tweets if any(name in tweet.lower() for name in candidates['kamalaHarris'])]
    pbt = [tweet for tweet in tweets if any(name in tweet.lower() for name in candidates['peteButtigieg'])]
    tst = [tweet for tweet in tweets if any(name in tweet.lower() for name in candidates['tomSteyer'])]
    tgt = [tweet for tweet in tweets if any(name in tweet.lower() for name in candidates['tulsiGabbard'])]
    
    p = [tweet for tweet in tweets if get_tweet_sentiment(tweet) == 'positive']
    n = [tweet for tweet in tweets if get_tweet_sentiment(tweet) == 'negative']
    pp = 100*len(p)/len(tweets)
    np = 100*len(n)/len(tweets)
    neutp = 100 - (100*len(p)/len(tweets)) - (100*len(n)/len(tweets))
    total = [pp, np, neutp]
    
    ayp = [tweet for tweet in ayt if get_tweet_sentiment(tweet) == 'positive']
    ayn = [tweet for tweet in ayt if get_tweet_sentiment(tweet) == 'negative']
    aypp = 100*len(ayp)/len(ayt)
    aynp = 100*len(ayn)/len(ayt)
    ayneutp = 100 - (100*len(ayp)/len(ayt)) - (100*len(ayn)/len(ayt))
    andrewYang = [aypp, aynp, ayneutp]
    
    akp = [tweet for tweet in akt if get_tweet_sentiment(tweet) == 'positive']
    akn = [tweet for tweet in akt if get_tweet_sentiment(tweet) == 'negative']
    akpp = 100*len(akp)/len(akt)
    aknp = 100*len(akn)/len(akt)
    akneutp = 100 - (100*len(akp)/len(akt)) - (100*len(akn)/len(akt))
    amyKlobuchar = [akpp, aknp, akneutp]
    
    bsp = [tweet for tweet in bst if get_tweet_sentiment(tweet) == 'positive']
    bsn = [tweet for tweet in bst if get_tweet_sentiment(tweet) == 'negative']
    bspp = 100*len(bsp)/len(bst)
    bsnp = 100*len(bsn)/len(bst)
    bsneutp = 100 - (100*len(bsp)/len(bst)) - (100*len(bsn)/len(bst))
    bernieSanders = [bspp, bsnp, bsneutp]

    cbp = [tweet for tweet in cbt if get_tweet_sentiment(tweet) == 'positive']
    cbn = [tweet for tweet in cbt if get_tweet_sentiment(tweet) == 'negative']
    cbpp = 100*len(cbp)/len(cbt)
    cbnp = 100*len(cbn)/len(cbt)
    cbneutp = 100 - (100*len(cbp)/len(cbt)) - (100*len(cbn)/len(cbt))
    coryBooker = [cbpp, cbnp, cbneutp]
    
    ewp = [tweet for tweet in ewt if get_tweet_sentiment(tweet) == 'positive']
    ewn = [tweet for tweet in ewt if get_tweet_sentiment(tweet) == 'negative']
    ewpp = 100*len(ewp)/len(ewt)
    ewnp = 100*len(ewn)/len(ewt)
    ewneutp = 100 - (100*len(ewp)/len(ewt)) - (100*len(ewn)/len(ewt))
    elizabethWarren = [ewpp, ewnp, ewneutp]

    jbp = [tweet for tweet in jbt if get_tweet_sentiment(tweet) == 'positive']
    jbn = [tweet for tweet in jbt if get_tweet_sentiment(tweet) == 'negative']
    jbpp = 100*len(jbp)/len(jbt)
    jbnp = 100*len(jbn)/len(jbt)
    jbneutp = 100 - (100*len(jbp)/len(jbt)) - (100*len(jbn)/len(jbt))
    joeBiden = [jbpp, jbnp, jbneutp]
    
    khp = [tweet for tweet in kht if get_tweet_sentiment(tweet) == 'positive']
    khn = [tweet for tweet in kht if get_tweet_sentiment(tweet) == 'negative']
    khpp = 100*len(khp)/len(kht)
    khnp = 100*len(khn)/len(kht)
    khneutp = 100 - (100*len(khp)/len(kht)) - (100*len(khn)/len(kht))
    kamalaHarris = [khpp, khnp, khneutp]
    
    pbp = [tweet for tweet in pbt if get_tweet_sentiment(tweet) == 'positive']
    pbn = [tweet for tweet in pbt if get_tweet_sentiment(tweet) == 'negative']
    pbpp = 100*len(pbp)/len(pbt)
    pbnp = 100*len(pbn)/len(pbt)
    pbneutp = 100 - (100*len(pbp)/len(pbt)) - (100*len(pbn)/len(pbt))
    peteButtigieg = [pbpp, pbnp, pbneutp]
    
    tsp = [tweet for tweet in tst if get_tweet_sentiment(tweet) == 'positive']
    tsn = [tweet for tweet in tst if get_tweet_sentiment(tweet) == 'negative']
    tspp = 100*len(tsp)/len(tst)
    tsnp = 100*len(tsn)/len(tst)
    tsneutp = 100 - (100*len(tsp)/len(tst)) - (100*len(tsn)/len(tst))
    tomSteyer = [tspp, tsnp, tsneutp]
    
    tgp = [tweet for tweet in tgt if get_tweet_sentiment(tweet) == 'positive']
    tgn = [tweet for tweet in tgt if get_tweet_sentiment(tweet) == 'negative']
    tgpp = 100*len(tgp)/len(tgt)
    tgnp = 100*len(tgn)/len(tgt)
    tgneutp = 100 - (100*len(tgp)/len(tgt)) - (100*len(tgn)/len(tgt))
    tulsiGabbard = [tgpp, tgnp, tgneutp]
    
    results = {'total': total}
    for candidate in candidates:
       results.update({candidate: eval(candidate)})
     
    return results

def display_results(results):
    print('Total results: \n' +
          'Positive tweet percentage: ' + str(results['total'][0])
          + '\n Negative tweet percentage: ' + str(results['total'][1])
          + '\n Neutral tweet percentage: '  + str(results['total'][2])
          + '\n')
    
    for n in range(1,len(results.keys()) - 1):
        print(str(candidates[list(candidates.keys())[n]][0].capitalize()) + ' ' +
              str(candidates[list(candidates.keys())[n]][1].capitalize()) + 
              '\'s results: \n Positive tweet percentage: ' + str(results[list(results.keys())[n]][0])
              + '\n Negative tweet percentage: ' + str(results[list(results.keys())[n]][1])
              + '\n Neutral tweet percentage: '  + str(results[list(results.keys())[n]][2])
              + '\n')
                
        
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

tweets = get_tweets("first.json")
results = results(tweets)
display_results(results)
