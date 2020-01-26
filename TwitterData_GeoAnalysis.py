#!/usr/bin/env python
# coding: utf-8

# In[51]:


import re 
import tweepy 
from tweepy import OAuthHandler  
import matplotlib.pyplot as plt
import json
import geopy
from geopy.geocoders import Nominatim   
import datetime
from elasticsearch import Elasticsearch
import pycountry
import time
from geopy.exc import GeocoderTimedOut
from textblob import TextBlob


# In[40]:


consumer_key = 'fvK9QDOLVp1CedyCR5Dz76wjZ'
consumer_secret = 'UBb22R7pwil0DSfvcdXI4NOWVwCSID1W8fkFHL0T9s0bxlTtCS'
access_token = '468385324-9yRxQ5yZGRAEQwCxDqtxBzz4jAbDOt9snLR5tRTh'
access_token_secret = 'Im0bJLSL4uY6Je7PlkNwQEwJg0BKcqKDUJwXtRZlpcSUQ'
auth = OAuthHandler(consumer_key, consumer_secret) 
auth.set_access_token(access_token, access_token_secret)    
api = tweepy.API(auth)
api.verify_credentials()
print("Authentication OK")


# In[41]:


class Client_Twitter(object):
  
	def __init__(self): 
			
			
			# keys and tokens from the Twitter Dev Console",
		consumer_key = 'fvK9QDOLVp1CedyCR5Dz76wjZ'
		consumer_secret = 'UBb22R7pwil0DSfvcdXI4NOWVwCSID1W8fkFHL0T9s0bxlTtCS'
		access_token = '468385324-9yRxQ5yZGRAEQwCxDqtxBzz4jAbDOt9snLR5tRTh'
		access_token_secret = 'Im0bJLSL4uY6Je7PlkNwQEwJg0BKcqKDUJwXtRZlpcSUQ'
		   
		try: 
				 
			self.auth = OAuthHandler(consumer_key, consumer_secret) 
			self.auth.set_access_token(access_token, access_token_secret)    
			self.api = tweepy.API(self.auth)
			api.verify_credentials()
			print("Authentication OK")
		except: 
			print("Error: Authentication Failed") 
                
            
	def get_tweets(self, query, count = 100): 
		tweets = [] 
		try: 
		 
			fetched_tweets = self.api.search(q = query, count = count)
			#(fetched_tweets[0])
			
			for tweet in fetched_tweets: 
				ttext = json.dumps(tweet._json)
				parsed = json.loads(ttext)
				tweets.append(parsed)
				
			   #parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 

			# return parsed tweets 
			return tweets 
		except tweepy.TweepError as e: 
			# print error (if any) 
			print("Error : " + str(e))
			
	def do_geocode(self,t):
		try:
			geolocator = Nominatim(user_agent="apa")
			location = geolocator.geocode(t)
			if location !=None:
				return([location.latitude, location.longitude])
		except GeocoderTimedOut:
			return self.do_geocode(t)

	def do_geocode_rev(self,latlong):
		try:
			geolocator = Nominatim(user_agent="apa")
			location = geolocator.reverse(latlong)
			if location !=None:
				#newloc= re.sub("[^a-zA-Z]+", "", location.address.split(",")[-1])
				return(location.address.split(",")[-1])
		except GeocoderTimedOut:
			return self.do_geocode_rev(latlong)

	def getCountryCode(self,check):
		try:
			df = pycountry.countries.search_fuzzy(data[str(i)]['con'])
			return df[0].numeric
		except:
			return 0
			
	def clean_tweet(self,tweet):
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())

	def get_tweet_sentiment(self, tweet):
		analysis = TextBlob(self.clean_tweet(tweet))
		if analysis.sentiment.polarity > 0:
			return 'positive'
		elif analysis.sentiment.polarity == 0:
			return 'neutral'
		else:
			return 'negative'