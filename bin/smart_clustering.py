from __future__ import division
import pandas as pd
import os
import numpy as np
from scipy.io import mmwrite
from scipy.io import mmread
from fuzzywuzzy import fuzz
from sklearn.cluster import DBSCAN

def smart_cluster_based_on_matrix(scipy_matrix, original_list):
    # takes is scipy matrix and the list  and returns a pandas df with the identified clusters
    clust = DBSCAN(eps=0.1, min_samples=1, metric="precomputed")
    clust.fit(scipy_matrix)
    # print cluster report
    preds = clust.labels_
    clabels = np.unique(preds)
    output = []
    for i in range(clabels.shape[0]):
        if clabels[i] < 0:
            continue
        cmem_ids = np.where(preds == clabels[i])[0]
        cmembers = []
        for cmem_id in cmem_ids:
            cmembers.append(original_list[cmem_id])
        #if clabels.shape[0] > 11:
        #    if i < 11:
        #        print("Cluster#%d: %s" % (i, ", ".join(cmembers)))
        #    elif i == 11:
        #        print("...")
        #else:
        #    print("Cluster#%d: %s" % (i, ", ".join(cmembers)))
        output.append(["Cluster#%d: %s" % (i, ", ".join(cmembers))])
    final_output = pd.DataFrame(output)
    return final_output