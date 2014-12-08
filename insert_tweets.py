#!/usr/bin/python

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import pymongo
from pymongo import MongoClient
import datetime

import json


#twitter_api = Twitter(language='en')
client = MongoClient()
db = client['tweetdb']
collection = db['tweets']

ckey = '9BISaQTrryl5V9wIOv56g'
csecret = 'aJeiFLbIiYFk8sb4TVsraw6zqjoEParQcrcSpZzY6U'
atoken = '2295205662-jOLHa9LbYXzsTpP61FXEVeRInpT6wVe01nK6HrW'
asecret = '0UtCBtu59c8wwHSJeyAuHCs7agGeSFccKRth1FhrlVt8G'

class listener(StreamListener):

    def on_data(self,data):
        try:
            tweet = json.loads(data)
            tweet_id = tweet["id"]
            print tweet["id"], tweet["coordinates"]
            if tweet["lang"] != "en":
                pass
            if collection.find({"tweet_id": tweet_id}).limit(1).count() == 0:
                
                text = tweet["text"]
                today = datetime.date.today()
                date = datetime.datetime.strptime(str(today), '%Y-%m-%d')
                tweet_coord = tweet["coordinates"]
                if tweet_coord != None:
                    print "position: ",tweet_coord["type"]
                my_tweet = {"tweet_id": tweet_id,
                            "text": text,
                            "date": date,
                            "coordinates": tweet_coord
                            }
                #this_tweet_id = collection.insert(my_tweet)
                if tweet_coord != None:
                    print my_tweet
            else:
                print "Error"
            return True

        except:
            pass

        return True


    def on_error(self,status):
        print status


auth = OAuthHandler(ckey,csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
common_filter = ['@','is','a','are','if','the','I','in','and']
twitterStream.filter(track=common_filter)

#twitterStream.filter(track=["car"])
'''
import pymongo
from pymongo import MongoClient
import datetime
from pattern.web import Twitter, plaintext


twitter_api = Twitter(language='en')
client = MongoClient()
db = client['tweetdb']
collection = db['tweets']

common_filter = ['@','is','a','are','@','if','the','I','in','and']

for item in common_filter:
    tweets = twitter_api.search(item, count=3000)
    for tweet in tweets:
        tweet_id = tweet.id
        if collection.find({"tweet_id": tweet_id}).limit(1).count() == 0:
            text = tweet.text
            tweet_date = tweet.date
            date = datetime.datetime.strptime(tweet_date, '%a %b %d %H:%M:%S +0000 %Y')
            my_tweet = {"tweet_id": tweet_id,
                        "text": text,
                        "date": date
                        }
            this_tweet_id = collection.insert(my_tweet)
            #print my_tweet
'''
