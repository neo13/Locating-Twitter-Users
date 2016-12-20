import json, random, os, math
from pymongo import MongoClient

import numpy as np

from db.GeoNamesCanada import GeoNamesCanada as gn

from scipy import optimize
from scipy.optimize import minimize_scalar, minimize


#size of the experiment
EXP_SIZE = 100

CITIES_LIST = ["toronto", "montreal", "calgary", "ottawa", "edmonton","mississauga", "winnipeg", "ajax", "brampton", "hamilton"]


DATA_FOLDER = "data/"

def get_distance(loc1, loc2):

	result = math.sqrt((loc1["lat"] - loc2["lat"])**2 + \
		(loc1["long"] - loc2["long"])**2)

	#print("returning " + result.__str__())
	return result

def select_tweets(total, num):
	res = []
	for i in range(num):
		res.append(random.randint(0, total - 1))

	return res

def get_file_path(filename):
    return DATA_FOLDER + filename


#this function reads the "filename" file from the data folder
#returns a list object containing all the tweets or users in the file
def parse_file(filename):
    f = open(get_file_path(filename))
    res = json.load(f)
    f.close()
    return res


def connect():
	#connect to mogno server and get a db object
	client = MongoClient('localhost', 27017)
	db = client.tweefind

	#get the collection object for venue names and info
	return db.venues


def predict_tweet(venues, tweet):
	#this function is in charge of predicting the location of a tweet 
	#based on the influence model info saved in the database
	all_locations = []

	words = tweet[0] + tweet[1]
	for word in words:
		if gn.lookup(word):
			res = venues.find_one({
					"name": word,
				})

			all_locations.append(res)


	def new_func(x):
		value = 1
		for item in all_locations:
			power_val = math.pow(item["lat"] - x[0], 2) + math.pow(item["long"] - x[1], 2)

			value = value * math.exp(power_val/(-2 * item["influence"] ** 2)) / ((2 * math.pi * item["influence"] ** 2))

		return (-1) * value

	argmin = minimize(new_func, x0 = np.array([56.1304, 106.3468]), method='nelder-mead',\
						options={'xtol': 1e-8, 'disp': True})


	return {
		"lat": argmin.x[0],
		"long": argmin.x[1],
	}


def check_prediction(venues, prediction, tweet):
	real_location = venues.find({
			"name": tweet[len(tweet) - 1].split(",")[0],
		})

	for city in CITIES_LIST: 

		city_obj = venues.find_one({
				"name": city,
			})
		if city_obj:
			if get_distance(prediction, city_obj) < 0.01:
				if city_obj.name == tweet[len(tweet) - 1].split(",")[0]:
					return True

	return False


def experiment():
	venues = connect()


	#variables for calculating accuracy
	total = 0
	correct = 0

	#iterate through all files in the data folder, choose tweets randomly,
	#predict the location of those tweets, and report accuracy
	for filename in os.listdir(DATA_FOLDER):
		if filename.endswith("-tweet.json"):
			tweets = parse_file(filename)
			inds = select_tweets(len(tweets), EXP_SIZE)
			for index in inds:
				prediction = predict_tweet(venues, tweets[index])
				if check_prediction(venues, prediction, tweets[index]):
					correct = correct + 1

	accuracy = correct/total
	print("Accuracy = " + accuracy.__str__())
	return accuracy


if __name__ == "__main__":
	accs = []
	for i in range(5):
		accs.append(experiment())

	av = 0
	for acc in accs:
		av = av + acc

	print(av/5)
