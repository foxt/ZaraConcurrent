#!/usr/bin/python

from pattern.web import Twitter, plaintext


twitter_api = Twitter(language='en')

tweets = twitter_api.search("@", count=2)
for tweet in tweets:
    text = tweet.text
    print text
