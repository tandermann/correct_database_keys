import pandas as pd
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


fossil_file = pd.read_csv('/Users/tobias/GitHub/correct_database_keys/data/joined_databases.txt',sep='\t',low_memory=False)
reference_database = pd.read_csv('/Users/tobias/GitHub/correct_database_keys/data/mammal_organismnames_unique.txt',sep='\t')
#fossil_file.head()
#reference_database.head()

sample_set_fossil_file = fossil_file.loc[:1500]
taxon_names = list(sample_set_fossil_file.name)

X = np.zeros((len(taxon_names), len(taxon_names)))

#for i in range(len(taxon_names)):
#    for j in range(len(taxon_names)):


for i in range(len(taxon_names)):
    #print every 100 rows info
    if i > 0 and i % 100 == 0:
        print("Processed %d/%d rows of data" % (i, X.shape[0]))
    for j in range(len(taxon_names)):
        if X[i, j] == 0.0:        
            X[i, j] = compute_similarity(taxon_names[i].lower(), taxon_names[j].lower())
            X[j, i] = X[i, j]

# write to Matrix Market format for passing to DBSCAN
mmwrite('/Users/tobias/GitHub/correct_database_keys/intermediate_files/taxon_sim_names.mtx', X)

X = mmread('/Users/tobias/GitHub/correct_database_keys/intermediate_files/taxon_sim_names.mtx')
clust = DBSCAN(eps=0.1, min_samples=1, metric="precomputed")
clust.fit(X)

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
        cmembers.append(taxon_names[cmem_id])
    output.append(["Cluster#%d: %s" % (i, ", ".join(cmembers))])

final_output = pd.DataFrame(output)
final_output.to_csv('/Users/tobias/GitHub/correct_database_keys/intermediate_files/clusters.txt', sep = '\t', index = False, header=False)
with open('/Users/tobias/GitHub/correct_database_keys/intermediate_files/clusters.txt', 'a') as file:
    file.write('Original number of categories: %i' %len(set(taxon_names)))


