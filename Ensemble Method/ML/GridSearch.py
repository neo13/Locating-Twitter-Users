import random
from sklearn.model_selection import GridSearchCV
from datetime import datetime
class GridSearch:
    def __init__(self, model, params, samples, lables):
        self.model = model
        self.params = params
        self.samples = samples
        self.lables = lables

    def search(self):
        print "Grid searh begins at (%s) ..." %(str(datetime.now()))
        chunk_size = int(self.samples.shape[0]*0.2)
        test_set_index = range(self.samples.shape[0])
        random.shuffle(test_set_index)
        search_sample_set = self.samples[test_set_index[0:chunk_size]]
        search_lable_set = self.lables[test_set_index[0:chunk_size]]
        self.grid = GridSearchCV(self.model, param_grid=self.params)
        self.grid.fit(search_sample_set, search_lable_set)
        print "Grid searh ends at (%s) ..." %(str(datetime.now()))
        return self.grid.best_params_