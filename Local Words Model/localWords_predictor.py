import pdb
import os
import json
import re
import sys
import math
from pymongo import MongoClient



DATA_FOLDER = "data/"


def get_file_path(filename):
    return DATA_FOLDER + filename


names = ["Edmonton, Alberta", "Calgary, Alberta", "Montral, Qubec", "Ottawa, Ontario", "Toronto, Ontario", "Mississauga, Ontario", 
"Winnipeg, Manitoba", "Ajax, Ontario", "Brampton, Ontario", "Hamilton, Ontario"]

client = MongoClient('localhost', 27017)
db = client.locatweet

#get the collection object for venue names and info

words = db.words

#number of the tweets per user
size = 10

corrects = 0

for item in os.listdir():
	if item.endswith(".json"):
		with open(item) as f:
			json_list = json.loads(f.readline())
			# pdb.set_trace()
			
			for i in range(0,size):
				bag_of_words = json_list[i]["text"].split(" ")
				probs = []
				for w in range(len(bag_of_words)):
					
					word = words.find({"word": bag_of_words[w]})
					if word.count() == 0:
						continue
					obj = word.next()
					probability = 0

					word_count = 0

					for it in bag_of_words:
						if it == bag_of_words[w]:
							word_count = word_count + 1
					
					for city in range(len(obj["cities"]) ):
						probability = probability + (obj["cities"][city]["prob"] * word_count)
						
					probs.append(probability)
				city ="None"
				for n in range(len(probs)):
					# print(probs)
					if max(probs) == probs[n]:
						city = names[n]
						break
				# print(city)
				if city == json_list[i]["user"]["location"]:
					corrects = corrects + 1

print(corrects)
accuracy = corrects/(size * 5000) 
print(accuracy)




			


