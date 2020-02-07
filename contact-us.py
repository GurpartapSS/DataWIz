from flask import Flask, request, render_template
from TwitterData_GeoAnalysis import Client_Twitter
import json
import re 
import tweepy 
from tweepy import OAuthHandler  
import matplotlib.pyplot as plt
import geopy
from geopy.geocoders import Nominatim   
import datetime
from elasticsearch import Elasticsearch
import pycountry
import time
from geopy.exc import GeocoderTimedOut

app = Flask(__name__, static_url_path='', 
            static_folder='static',
            template_folder='templates')

@app.route('/')
def contactForm():

	
	return render_template("index.html",value=[])
	
	
@app.route('/update/',methods=["GET"])
def contactSave():


	api = Client_Twitter()
	#loc = Location()
	tweets = api.get_tweets(query = '#corona', count = 100)
	
	test_tw = []
	for tweet in tweets:
		parsed_tweet = {}
		parsed_tweet['text'] = tweet['text']
		parsed_tweet['sentiment'] = api.get_tweet_sentiment(tweet['text'])
		if tweet['retweet_count'] > 0:
			if parsed_tweet not in test_tw:
				test_tw.append(parsed_tweet)
		else:
			test_tw.append(parsed_tweet)
	
	print("Tweets Retrieved from Twitter")
	
	str_list = [[t["user"]["location"],datetime.datetime.strptime(t["user"]["created_at"], '%a %b %d %H:%M:%S %z %Y').strftime('%Y-%m-%d %H:%M:%S')] for t in tweets] 

	str_new_list= [[i,j] for i,j in str_list if i!=""]

	doc={}
	test_dict={}
	#test time
	#tic = time.clock()
	for i,t in enumerate(str_new_list):
		vari = api.do_geocode(t[0])
		if(vari):
			#test
			country = api.do_geocode_rev("{}, {}".format(vari[0],vari[1]))
			test_dict['location{}'.format(i)]={"lat":vari[0],"lon":vari[1], "con": country,"DaTime":t[1]}
			#doc['location']={"lat":vari[0],"lon":vari[1], "con": country,"DaTime":t[1]}
			#toc = time.clock()
			#print(toc-tic)
	
	print("Build Dictionary Done")	
	import json	
	json = json.dumps(test_dict)
	f = open("test_data.json","w")
	f.write(json)
	f.close()
	import json
	json = json.dumps({"ttext":[t["text"] for t in tweets]})
	f = open("text_test_data.json","w")
	f.write(json)
	f.close()
	import json
	f = open("test_data.json","r")
	data = json.load(f)
	f.close()

	print("Data written to json file")	
	es=Elasticsearch([{'host':'localhost','port':9200}])

	for i in data:
		doc = {
			"location": {
				"lat": data[str(i)]['lat'],
				"lon": data[str(i)]['lon']
			},
			"country": data[str(i)]['con'],
			"country_code": api.getCountryCode(data[str(i)]['con']),
			"date": data[str(i)]['DaTime']
			
		}
		res = es.index(index="datawiz", body=doc)

	print("Data written to ElasticSearch")
	
	return render_template("index.html",value=test_tw)
	
if __name__ == "__main__":
    app.run(host="localhost")
	


	