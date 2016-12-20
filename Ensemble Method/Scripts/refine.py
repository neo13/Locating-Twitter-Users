import os, re, json, csv, symbols
sys.path.append('../')

from nltk.corpus import stopwords
from GeoNamesCanada import GeoNamesCanada as gn

ls = ["Ajax, Ontario", "Calgary, Alberta", "Montral, Qubec", "Ottawa, Ontario", "Toronto, Ontario"]
for name in ls:
    data_source = "../corpus/%s" %name
    tweet_json = "../dataset/%s-tweet.json" %name
    user_json = "../dataset/%s-user.json" %name
    location = name
    tweets = []
    users = []

    for root, dirs, filenames in os.walk(data_source):
        i = 1
        lenght = len(filenames)
        for file_name in filenames:
            #we get user id from file name
            print "processing file %s (%s/%s)" %(file_name, str(i), lenght)
            i += 1
            #we get user id from file name
            uid = re.split(r'\.', file_name)[0]
            #create path of file
            file_path = os.path.join(data_source, file_name)

            #readfile and decode json
            with open(file_path, "r") as data_file:
                data = json.load(data_file)

            #go through all the twittes and get remove all unused data and keep all the needed data
            for tweet in data:
                #information that we need are [bag of words, bag of locations, hashtags, links, symbols]

                #extract and create bag of words
                #remove links
                text = re.sub(r'https?:\/\/.*[\r\n]*[\s]', '', tweet['text'])
                #remove nonalphabetic words
                letters_only = re.sub("[^a-zA-Z]", " ", text)
                words = letters_only.lower().split()
                stops = set(stopwords.words("english"))
                #remove stopwords
                bag_of_words = [w for w in words if not w in stops]

                #extract bag of locations
                bag_of_location = []
                for word in bag_of_words:
                    if gn.lookup(word):
                        bag_of_location.append(word)
                        bag_of_words.remove(word)

                #extract hashtags
                hashtags = tweet['entities']['hashtags']

                #extract links
                urls = tweet['entities']['urls']

                #extract symbols
                symbols = tweet['entities']['symbols']

                #extract coordinates
                coordinates = tweet['coordinates']

                _tweet = [bag_of_words, bag_of_location, hashtags, urls, symbols, coordinates, tweet['created_at'], location]  
                tweets.append(_tweet)

            #append user to users
            user = [data[0]['user']['id'], data[0]['user']['location'], data[0]['user']['time_zone'], data[0]['user']['lang'], len(data), location]
            users.append(user)

    with open(tweet_json, "w") as fout:
        fout.write(json.dumps(tweets))

    with open(user_json, "w") as fout:
        fout.write(json.dumps(users))