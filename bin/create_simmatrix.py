from __future__ import division
import os
import numpy as np
from scipy.io import mmwrite
from scipy.io import mmread
from fuzzywuzzy import fuzz
from sklearn.cluster import DBSCAN

def compute_similarity(s1, s2):
    return 1.0 - (0.01 * max(
        fuzz.ratio(s1, s2),
        fuzz.token_sort_ratio(s1, s2),
        fuzz.token_set_ratio(s1, s2)))
        
def create_simmatrix(list_of_strings):
    X = np.zeros((len(list_of_strings), len(list_of_strings)))
    for i in range(len(list_of_strings)):
        #print every 100 rows info
        if i > 0 and i % 100 == 0:
            print("Processed %d/%d rows of data" % (i, X.shape[0]))
        for j in range(len(list_of_strings)):
            if X[i, j] == 0.0:        
                X[i, j] = compute_similarity(list_of_strings[i].lower(), list_of_strings[j].lower())
                X[j, i] = X[i, j]
    return X
    