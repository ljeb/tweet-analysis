import json
import re
from textblob import TextBlob
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()

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

validLocations = ["AL", "Alabama", "AK", "Alaska", "AZ", "Arizona",
                  "AR", "Arkansas", "CA", "California", "CO", "Colorado",
                  "CT", "Connecticut", "DC", "D.C.", "DE", "Delaware",
                  "FL", "Florida", "GA", "Georgia", "HI", "Hawaii",
                  "ID", "Idaho", "IL", "Illinois", "IN", "Indiana",
                  "IA", "Iowa", "KS", "Kansas", "KY", "Kentucky", 
                  "LA", "Louisiana", "ME", "Maine", "MD", "Maryland",
                  "MA", "Massachusetts", "MI", "Michigan", 
                  "MN", "Minnesota", "MS", "Mississippi", "MO", "Missouri",
                  "MT", "Montana", "NE", "Nebraska", "NV", "Nevada",
                  "NH", "New Hampshire", "NJ", "New Jersey", "NM", "New Mexico",
                  "NY", "New York", "NC", "North Carolina", "ND", "North Dakota",
                  "OH", "Ohio", "OK", "Oklahoma", "OR", "Oregon", 
                  "PA", "Pennsylvania", "RI", "Rhode Island",
                  "SC", "South Carolina", "SD", "South Dakota", "TN", "Tennessee",
                  "TX", "Texas", "UT", "Utah", "VT", "Vermont", "VA", "Virginia",
                  "WA", "Washington", "WV", "West Virginia", "WI", "Wisconsin",  
                  "WY", "Wyoming", "U.S.A", 'United States']



def get_tweets(file_name):
    f = open(file_name)
    tweets = [json.loads(line) for line in f]
    f.close()
    filteredTweets = set()
    states = {validLocations[n]: 0 for n in range(0, len(validLocations)-3, 2)}

    for tweet in tweets:
        if 'text' in list(tweet.keys())     \
        and 'retweeted_status' not in tweet \
        and tweet['user']['location']       \
        and any(loc in tweet['user']['location'] for loc in validLocations):
            filteredTweets.add(clean_tweet(tweet['text']))
            for loc in tweet['user']['location'].split(','):
                if loc in validLocations[:-2]:
                    ind = validLocations.index(loc)
                    if loc == "Washington" and tweet['user']['location'] != "Washington, DC":
                        states['WA'] += 1
                    elif tweet['user']['location'] == "Washington, DC":
                        states['DC'] += 1 
                    elif not ind%2:
                        states[validLocations[ind]] += 1
                    else:
                        states[validLocations[ind-1]] += 1
    return filteredTweets, states

def get_results(tweets):
    p = [tweet for tweet in tweets if get_tweet_sentiment(tweet) == 'positive']
    n = [tweet for tweet in tweets if get_tweet_sentiment(tweet) == 'negative']
    pp = 100*len(p)/len(tweets)
    np = 100*len(n)/len(tweets)
    neutp = 100 - (100*len(p)/len(tweets)) - (100*len(n)/len(tweets))
    total = [pp, np, neutp]
    return total
    
def results(tweets):
    results = {}
    ctweets = {candidate: [tweet for tweet in tweets if any(name in tweet.lower() 
               for name in candidates[candidate])] for candidate in candidates}
    results = {candidate:get_results(ctweets[candidate]) for candidate in ctweets}       
    results.update({'total':get_results(tweets)})  
    return results

def display_results(results, states):
    print('Total results: '
          + '\n Positive tweet percentage: ' + str(results['total'][0])
          + '\n Negative tweet percentage: ' + str(results['total'][1])
          + '\n Neutral tweet percentage: '  + str(results['total'][2])
          + '\n')
    for n in range(len(results.keys()) - 2):
        print(str(candidates[list(candidates.keys())[n]][0].capitalize()) + ' ' +
              str(candidates[list(candidates.keys())[n]][1].capitalize()) + 
              '\'s results: \n Positive tweet percentage: ' + str(results[list(results.keys())[n]][0])
              + '\n Negative tweet percentage: ' + str(results[list(results.keys())[n]][1])
              + '\n Neutral tweet percentage: '  + str(results[list(results.keys())[n]][2])
              + '\n')
    print('State count:')
    for state in states:
        print(' Number of tweets from ' + str(state) + ': ' + str(states[state]))
                
        
def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def get_tweet_sentiment(tweet):
    analysis = TextBlob(tweet)
    return 'positive' if analysis.sentiment.polarity > 0 else 'neutral' if analysis.sentiment.polarity == 0 else 'negative'
    
#def get_tweet_sentiment(tweet):
#    analysis = sid.polarity_scores(tweet)
#    return 'positive' if analysis['compound'] > 0 else 'neutral' if analysis['compound'] == 0 else 'negative'

tweets, states = get_tweets("first.json")
results = results(tweets)
display_results(results, states)
