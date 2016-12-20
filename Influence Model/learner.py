#This file is in charge of reading all records from the database
#and calculating the influence for all the locations whose influence
# is currently set to -1, i.e. not calculated.

#import pdb for debuggins purposes
import pdb

#for mathematical functions
import math

#optimization packages for obtaining argmax of influence function 
from scipy.optimize import minimize_scalar, minimize
from pymongo import MongoClient


def connect():
	#connect to mogno server and get a db object
	client = MongoClient('localhost', 27017)
	db = client.tweefind

	#get the collection object for venue names and info
	return db.venues



def get_distance(loc1, loc2):

	result = math.sqrt((loc1["lat"] - loc2["lat"])**2 + \
		(loc1["long"] - loc2["long"])**2)

	#print("returning " + result.__str__())
	return result


def get_influence_function(location):
	power_val = 0
	total_tweets = 0

	#calculate the power_value of the influence function
	# and the total number of tweets about a venue
	for item in location["tweets"]:
		power_val = power_val + get_distance(location, item) * item["number"]
		total_tweets = total_tweets + item["number"]

	#scale down the values of total tweets and power val
	power_val = power_val / 1000
	total_tweets = total_tweets / 1000

	#print(power_val)
	#print(total_tweets)

	#define function to be optimized here.
	def new_func(mu):
		return (-1) * math.exp(power_val/(-2 * mu ** 2)) / ((2 * math.pi * mu ** 2) ** total_tweets)

	return new_func


def update_all_influences():

	venues = connect()

	#find all venues whose influence has not been set yet.
	for location in venues.find({"influence": -1}):
		func = get_influence_function(location)

		alpha = minimize_scalar(func, bounds=(1, 10000000), method='bounded')
		
		continue

		venues.update({
				"name": location["name"],
			}, {
				"influence": alpha.x
			})


if __name__ == "__main__": 
	update_all_influences()