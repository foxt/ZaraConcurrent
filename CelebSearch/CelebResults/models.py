from django.db import models

from pattern.web import Twitter, plaintext
from pattern.en import sentiment
import pymongo
from pymongo import MongoClient

class Clips_Adaptor(models.Model):
    '''
    Adaptor class for the CLiPS pattern package
    '''
    def search_tweets(self, celeb):
        '''
        Pull tweets from the Twitter API that mention 
        the given celebrity
        '''
        twitter_api = Twitter(language='en')
        #TODO: up the count for the final project
        return twitter_api.search(celeb, count=3000)

    def get_sentiment(self, tweets):
        '''
        Perform sentiment analysis on the given dict of tweets
        '''
        scores = []
        for tweet in tweets:
            score = sentiment(tweet["text"])
            scores.append(score)
        return scores

    def get_sentiment_concur(self, tweet):
        '''
        Perform sentiment analysis on a single tweet
        '''
        return str(sentiment(tweet["text"]))



class Mongo_Service(models.Model):
    '''
    Adaptor class to access the Mongo database
    '''
    client = ''
    db = ''
    collection = ''

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client['tweetdb']
        self.collection = self.db['tweets']

    def search_tweets(self, celeb):
        '''
        Searches tweets database based on the given celebrity.
        '''
        result = []
        for tweet in self.collection.find({"text": {"$regex": celeb, "$options": "-i"}},{"text": 1, "date": 1, "coordinates": 1, "_id": 0}):
            result.append(tweet)
            '''
            try:
                print tweet["coordinates"]
            except:
                pass
            '''
        return result


