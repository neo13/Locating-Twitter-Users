from api import API
import json, os
# from pymongo import MongoClient
import time

api_handle = API('tokens.json')
city_index = 42
stream = open('res.json', "r+")
raw = stream.read()
cities = json.loads(raw)
# client = MongoClient('0.0.0.0', 27017)
# db = client['twitter']
# tweets_collection = db['tweets']
# users = db['users']

while True:
    timestamp1 = time.time()
    for api in api_handle:
        max_id = ""
        folder_name = "data/" + cities["cities"][city_index]['full_name'].encode('ascii', 'ignore')
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        print("starting the next api ...")
        try:
            for i in range(0, 18):
                geo_q = str(cities["cities"][city_index]["centroid"][1]) + ","+ str(cities["cities"][city_index]["centroid"][0]) + ",5mi"
                print("getting tweets for %s" %geo_q)
                tweets = api.api.search.tweets(geocode=geo_q, result_type="recent", count=50, max_id=max_id)
                max_id = tweets['statuses'][-1]['id_str']
                for tweet in tweets['statuses']:
                    #tweet['city_lable'] = cities["cities"][city_index]['full_name']
                    tweet['user']['city_lable'] = cities["cities"][city_index]['full_name']
                    # try:
                    #     tweets_collection.insert_one(tweet)
                    # except Exception, e:
                    #     pass
                    # try:
                    #     users.insert_one(tweet["user"])
                    # except Exception, e:
                    #     pass
                    time_line = api.api.statuses.user_timeline(user_id=tweet["user"]["id"], count=200)
                    # for t in time_line:
                    #     try:
                    #         tweets_collection.insert_one(t)
                    #     except Exception, e:
                    #         pass
                    file_name = folder_name + "/" + str(tweet["user"]["id"]) + ".json"
                    with open(file_name, "w") as outfile:
                        outfile.write(json.dumps(time_line))
        except Exception, e:
            print(str(e));
            pass
        city_index = (city_index + 1)%100
    print("time to sleep ...")
    timestamp2 = time.time()
