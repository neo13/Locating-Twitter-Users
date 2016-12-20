#!/usr/bin/python
#this file loads all the location names in Canada, into a mongo db collection called "venues"
import re
import os

from pymongo import MongoClient
from filetools import parse_file, DATA_FOLDER
from GeoNamesCanada import GeoNamesCanada as gn


ALREADY_PROCESSED = ["Ajax, Ontario-tweets.json", ]


def connect():
	#connect to mogno server and get a db object
	client = MongoClient('localhost', 27017)
	db = client.tweefind

	#get the collection object for venue names and info
	return db.venues


#this function queries a given name from db, and returns the location of the name
def get_location_by_name(venues, name):
	if gn.lookup(name):
		res = venues.find_one({"name": name.lower()})
		if res:
			return {
				"lat": res["lat"],
				"long": res["long"],
			}

		else:
			return None

	return None



def get_location_name(name):
	if len(name) <= 4:
		is_location_name = gn.lookup(name)
		if is_location_name:
			return name
		else:
			return None
	else:
		for i in range(4, len(name)):
			is_location_name = gn.lookup(name[:i+1])
			if is_location_name:
				return name[:i+1]


	return None



#this function return all the location related words in a tweet
def get_all_tweet_words(tweet):
	#this function can be modified later for reading different parts of the tweet.

	#return all location words in the tweet
	#final_words_list = []
	# for word in tweet[0]:
	# 	final_words_list.append(word)
	# for word in tweet[1]:
	# 	final_words_list.append(word)

	return tweet[0] + tweet[1]


#this function updates the "tweets" key for all venues in db
def update_venue_tweets(venues, words, tweet_location):
	for word in words:
		geo_name = get_location_name(word)

		#if the word exists in the database, update the "tweets" list in the database
		if geo_name:
			print(geo_name)

			venue = venues.find_one({"name": geo_name})
			venue_tweets = venue["tweets"]

			print("VENEU TWEETS BEFORE EDITING")
			print(venue_tweets)
			print("TWEET_LOCATION")
			print(tweet_location)


			#variable to check if we updated the tweets list
			updated = False

			for item in venue_tweets:
				if item["lat"] == tweet_location["lat"] and \
					item["long"] == tweet_location["long"]:
					updated = True
					item["number"] = item["number"] + 1

			#if venue_tweets isn't updated, we need to add an item to venue_tweets
			if not updated:
				venue_tweets.append({
						"lat": tweet_location["lat"],
						"long": tweet_location["long"],
						"number": 1,
					})

			print("VENEU TWEETS AFTER EDITING")
			print(venue_tweets)


			venues.update({
				"name": word
			}, {
				"$set": {
					"tweets": venue_tweets,
				}
			})



#this function reads all venue names from CA.txt and stores them in mongodb along with 
#their coordinates
def load_venues(venues):

	#this file originally contained 327279 location names referring to differet
	#places on Canada's map. After removing duplicate items, we have unique names 
	#and locations in our collection.

	input_file = "CA.txt"
	with open(input_file, "r") as finput:
		for line in finput:
			bag = re.split(r'\t', line)

			altnames = [name for name in re.split(r',+', bag[3]) if name != '']
			altnames.append(bag[2])
			for name in altnames:

				venue = get_location(venues, name)
				if venues.count() > 0:
					continue
					
				else:
					venues.insert_one({
						"name": name.lower(),
						"lat": float(bag[4]),
						"long": float(bag[5]),
						"tweets": [],
						"influence": -1,
					})


#this function reads all preprocessed files to update info on venues in the db
def load_tweets(venues):
	import time
	for filename in os.listdir(DATA_FOLDER):
		if filename.endswith("-tweet.json"):

			#start calculating time to report elapsed time for processing every file
			start = time.time()

			#read file from disk
			tweets_list = parse_file(filename)

			#print information about file
			print("file: " + filename + " containing " + len(tweets_list).__str__() + " tweets...")

			#skip files that have been processed in earlier runs
			if filename in ALREADY_PROCESSED:
				print("Skipping " + filename)
				continue


			counter = 0

			#iterate over all tweets in the file
			for i, tweet in enumerate(tweets_list):

				counter = counter + 1

				#get all words from the file
				words = get_all_tweet_words(tweet)

				#get the location of the tweet, "city name"
				tweet_location = tweet[len(tweet) - 1].split(", ")[0]


				update_venue_tweets(venues, words, get_location_by_name(venues, tweet_location))

				if counter % 1000 == 0:
					print("So far handled " + counter.__str__() + " tweets.")

			end = time.time()
			elapsed = end - start
			print("done with file: " + filename + " in " + elapsed.__str__())
			exit()




#this part makes calls to the above functions
if __name__== "__main__":
	print("connecting to database...")
	venues = connect()
	#print("connection successful. adding venue names to mongodb...")
	#load_venues(venues)
	print("adding venue names to mongodb successful. loading tweets into mondodb...")
	load_tweets(venues)