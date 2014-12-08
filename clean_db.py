#!/usr/bin/python
'''
A script to remove tweets from the mongo 
database deemed too old
'''

import pymongo
from pymongo import MongoClient
import datetime

client = MongoClient()
db = client['tweetdb']
collection = db['tweets']

today = datetime.date.today()
ex_date = today - datetime.timedelta(days=7)
ex_date = datetime.datetime.strptime(str(ex_date), '%Y-%m-%d')
for tweet in collection.find({"date": {"$gt" : ex_date}},{"date":1}):
    collection.remove({"_id": tweet["_id"]})
    #print tweet

