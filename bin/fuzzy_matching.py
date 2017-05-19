import sys
sys.path
sys.path.append("./bin")
import create_simmatrix
import pandas as pd
from scipy.io import mmwrite

fossil_file = pd.read_csv('/Users/tobias/GitHub/correct_database_keys/data/joined_databases.txt',sep='\t',low_memory=False)

#reduce the original dataset to the first 1050 lines, for faster computation
sample_set_fossil_file = fossil_file.loc[:1050]
taxon_names = list(sample_set_fossil_file.name)

matrix = create_simmatrix.create_simmatrix(taxon_names)

# write to Matrix Market format for passing to DBSCAN
mmwrite('/Users/tobias/GitHub/correct_database_keys/intermediate_files/taxon_sim_names.mtx', matrix)

import smart_clustering
from IPython.display import display, HTML
from scipy.io import mmread

matrix = mmread('/Users/tobias/GitHub/correct_database_keys/intermediate_files/taxon_sim_names.mtx')

clusters = smart_clustering.smart_cluster_based_on_matrix(matrix,taxon_names)

display(clusters.head(10))
#clusters.head(10).to_html()

clusters.to_csv('/Users/tobias/GitHub/correct_database_keys/intermediate_files/clusters.txt', sep = '\t', index = False, header=False)
with open('/Users/tobias/GitHub/correct_database_keys/intermediate_files/clusters.txt', 'a') as file:
    file.write('Original number of categories: %i' %len(set(taxon_names)))

