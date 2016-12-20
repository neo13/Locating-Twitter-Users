import math
class score:
    def __init__(self, predictions, lables):
        self.TP = 0
        self.TN = 0
        self.FP = 0
        self.FN = 0

        for y, yhat in zip(lables, predictions):
            if y == 1 :
                if yhat == 1:
                    self.TP += 1
                else:
                    self.FN += 1
            else:
                if yhat == 1:
                    self.FP += 1
                else:
                    self.TN += 1

    def get_recall(self):
        return float(self.TP)/(self.TP + self.FN)

    def get_precision(self):
        return float(self.TP)/(self.TP + self.FP)

    def get_specificity(self):
        return float(self.TN)/(self.FP + self.TN)

    def get_NPV(self):
        return float(self.TN)/(self.FN + self.TN)

    def get_FPR(self):
        return 1-self.get_specificity()

    def get_FDR(self):
        return 1-self.get_precision()

    def get_FNR(self):
        return 1-self.get_recall()

    def get_accuracy(self):
        return float(self.TP + self.TN)/(self.TP + self.TN + self.FP + self.FN)

    def get_f1(self):
        return float(self.TP + self.TP)/(self.TP + self.TP + self.FP + self.FN)

    def get_fbeta(self, beta):
        return float((1+beta*beta) * self.TP)/((1+beta*beta) * self.TP + self.FP + (beta*beta) * self.FN)       

    def get_MCC(self):
        if (self.TP + self.TP) * (self.TP + self.FN) * (self.TN + self.FP) * (self.TN + self.FN) == 0:
            return 0
        else:
            return float(self.TP * self.TN - self.FP * self.FN)/math.sqrt((self.TP + self.TP) * (self.TP + self.FN) * (self.TN + self.FP) * (self.TN + self.FN))