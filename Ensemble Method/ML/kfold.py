from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.metrics import roc_curve, auc, confusion_matrix
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import *
from scipy import interp
from numpy.random import rand
from numpy import linspace, newaxis, arange
import matplotlib.pyplot as plt
from datetime import datetime
from score import score
from itertools import product
class kfold:
    def __init__(self, model, samples, lables, folds=10):
        self.model = model
        self.samples = samples
        self.lables = lables
        self.folds = folds

    def fit(self):
        print "kfold begins at (%s) ..." %(str(datetime.now()))
        self.results = {"roc": [], "scores": [], "CM": []}
        self.skf = KFold(n_splits=self.folds, shuffle=True)
        for index, (train_index, test_index) in enumerate(self.skf.split(self.samples, self.lables)):
            #OS = RandomOverSampler(ratio='auto')
            OS = RandomUnderSampler()
            #nm1x, nm1y = NM1.fit_sample(x, y)
            osx, osy = OS.fit_sample(self.samples[train_index], self.lables[train_index])
            print "fold %d begins at (%s) ..." %(index, str(datetime.now()))    
            print "train to test rate= (%d/%d)"%(sum(self.lables[train_index]), sum(self.lables[test_index]))
            self.model.fit(osx,osy)

            prediction = self.model.predict(self.samples[test_index])
            fpr, tpr, thresholds = roc_curve(self.lables[test_index], prediction, pos_label=1)
            self.results['roc'].append((fpr, tpr, thresholds))
            cm = confusion_matrix(self.lables[test_index], prediction)
            self.results['CM'].append(cm)

            sc = score(prediction, self.lables[test_index])
            self.results['scores'].append(sc)
        return self.results

    def ROC(self):
        mean_tpr = 0.0
        mean_fpr = linspace(0, 1, 100)
        for index, roc in enumerate(self.results['roc']):
            mean_tpr += interp(mean_fpr, roc[0], roc[1])
            mean_tpr[0] = 0.0
            roc_auc = auc(roc[0], roc[1])
            plt.plot(roc[0], roc[1], lw=1, color=rand(3), label='ROC fold %d (area = %0.2f)' % (index, roc_auc))
        plt.plot([0, 1], [0, 1], linestyle='--', lw=1, color='k', label='Luck')
        mean_tpr /= self.folds
        mean_tpr[-1] = 1.0
        mean_auc = auc(mean_fpr, mean_tpr)
        plt.plot(mean_fpr, mean_tpr, color='g', linestyle='--', label='Mean ROC (area = %0.2f)' % mean_auc, lw=1)
        plt.xlim([-0.05, 1.05])
        plt.ylim([-0.05, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver operating characteristic')
        plt.legend(loc="lower right")
        plt.show()

    def CM(self):
        fig = plt.figure()
        classes = ["PM", "~PM"]
        for index, cm in enumerate(self.results['CM']):
            plt.subplot(341 + index)
            plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
            plt.colorbar()
            tick_marks = arange(len(classes))
            plt.xticks(tick_marks, classes)
            plt.yticks(tick_marks, classes)
            cm = cm.astype('float') / cm.sum(axis=1)[:, newaxis]
            thresh = cm.max() / 2.
            for i, j in product(range(cm.shape[0]), range(cm.shape[1])):
                plt.text(j, i, "%.3f" %(cm[i, j]), horizontalalignment="center",color="white" if cm[i, j] > thresh else "black")
            plt.ylabel('True label')
            plt.xlabel('Predicted label')
        plt.show()
