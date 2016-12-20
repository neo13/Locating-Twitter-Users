import warnings
warnings.filterwarnings("ignore")

from sklearn.feature_extraction.text import CountVectorizer
from os import path
import json
from urlparse import urlparse
from datetime import datetime
from dateutil import parser
import numpy as np

TPU = 200
with open('sites.json', 'r') as fin:
    top_sites = json.load(fin)

ls = ["Ajax, Ontario", "Calgary, Alberta", "Montral, Qubec", "Ottawa, Ontario", "Toronto, Ontario"]
label = {
    "Ajax, Ontario": [0, 0],
    "Calgary, Alberta": [1, 1]
    "Montral, Qubec": [2, 2]
    "Ottawa, Ontario": [3, 0]
    "Toronto, Ontario": [4, 0]
} 
raw_dataset = []
for name in ls:
    tweet_json = "dataset/%s-tweet.json" %name
    user_json = "dataset/%s-user.json" %name

    idx = 0
    with open(user_json, "r") as fin:
        users = json.load(fin)
        with open(tweet_json, 'r') as fin:
            tweets = json.load(fin)
            for user in users:
                if user[4] < TPU:
                    continue;
                else:
                    u_tweets = tweets[idx:idx+TPU]
                    idx += user[4]
                    raw_dataset += [" ".join([" ".join(tweet[0]) for tweet in u_tweets]),
                                    " ".join([" ".join(tweet[1]) for tweet in u_tweets]),
                                    " ".join([" ".join([hashtag['text'] for hashtag in tweet[2]]) for tweet in u_tweets]),
                                    [int(parser.parse(tweet[6]).strftime("%H"))*60 + int(parser.parse(tweet[6]).strftime("%M")) for tweet in u_tweets]
                                    lables[user[5]][0], lables[user[5]][1]
                                    ]

word_vt = CountVectorizer(max_features=2000, binary=True, dtype=np.int16)
localname_vt = CountVectorizer(max_features=1000, binary=True, dtype=np.int16)
hashtag_vt = CountVectorizer(max_features=500, binary=True, dtype=np.int16)

vocab = dict()

print "vectorizing word set ..."
vectorized_word_set = word_vt.fit_transform(raw_dataset[0]).toarray()
vocab['words'] = word_vt.get_feature_names()

print "vectorizing local names ..."
vectorized_local_name_set = localname_vt.fit_transform(raw_dataset[1]).toarray()
vocab['local'] = localname_vt.get_feature_names()

print "vectorizing hashtags ..."
vectorized_hashtag_set = hashtag_vt.fit_transform([' '.join(raw_dataset[2]).toarray()
vocab['hashtag'] = hashtag_vt.get_feature_names()

print "saving dataset ..."
np.save('../dataset/words', vectorized_word_set)
np.save('../dataset/local', vectorized_local_name_set)
np.save('../dataset/hashtag', vectorized_hashtag_set)
np.save('../dataset/timestamp', np.array(raw_dataset[:, 3])
np.save('../dataset/labels', np.array(raw_dataset[:, 4])

print "done!"