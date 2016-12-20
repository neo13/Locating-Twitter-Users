#!/usr/bin/python
import re
import sys
import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)

if len(sys.argv) >= 2:
	input_file = sys.argv[1]
else:
	input_file = "CA.txt"

with open(input_file, "r") as finput:
	for line in finput:
		bag = re.split(r'\t', line)
		#name.decode('ascii', 'ignore').encode('ascii', 'ignore')
		altnames = [name for name in re.split(r',+', bag[3]) if name != '']
		altnames.append(bag[2])
		for name in altnames:
			r.set(name, bag[0].lower())
