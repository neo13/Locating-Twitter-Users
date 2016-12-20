# -*- coding: utf-8 -*-
import scipy.stats as stats
import matplotlib.pyplot as plt
import numpy as np
import json
words = np.load("vectorize_url.npy")
y = np.load("vectorize_city_lable.npy")
with open("vocab.json", "r") as fin:
    vocab = json.load(fin)
classes = vocab['city']
v_words = vocab['words']
ssum = np.sum(words, axis=0)
locat_terms_idx = []
for index, c in enumerate(classes):
  i = np.where(y == index)
  sub_words = words[i[0], :]
  fsum = np.sum(sub_words, axis=0)
  c_p = np.true_divide(fsum, ssum)
  idx = np.argsort(c_p)
  c_p.sort()
  locat_terms_idx += idx[np.where(c_p > 0.5)]
print locat_terms_idx