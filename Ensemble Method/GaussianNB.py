#!/usr/bin/python2.7
from numpy import average
from sklearn.naive_bayes import GaussianNB
from ML import kfold as kf, GridSearch as gs

#load data
samples = load(sys.argv[1])
lables = load("labels.npy")

folds = int(sys.argv[2]) if sys.argv[2] else 10

#DecisionTreeClassifier
clf = GaussianNB()
kfold = kf(clf, samples, lables, folds)
res = kfold.fit()
for score in kfold.results['scores']:
    print score.get_accuracy()
print average([score.get_accuracy() for score in kfold.results['scores']])