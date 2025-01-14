
import skchem
import pandas as pd
from scipy import io
train_path = './tox21_sdf/tox21_10k_data_all.sdf'
test_path = './tox21_sdf/tox21_10k_challenge_score.sdf'
train = skchem.io.sdf.read_sdf(train_path, error_bad_mol=False, warn_bad_mol=True, nmols=None, skipmols=None,
skipfooter=None, read_props=True, mol_props=False)
test = skchem.io.sdf.read_sdf(test_path, error_bad_mol=False, warn_bad_mol=True, nmols=None, skipmols=None,
skipfooter=None, read_props=True, mol_props=False)

#print (train.index)
#print (test.index)

print set(train.index).intersection(set(test.index))


y_tr = pd.read_csv('./tox21/tox21_labels_train.csv.gz', index_col=0, compression="gzip")
y_te = pd.read_csv('./tox21/tox21_labels_test.csv.gz', index_col=0, compression="gzip") 
x_tr_dense = pd.read_csv('./tox21/tox21_dense_train.csv.gz', index_col=0, compression="gzip")
x_te_dense = pd.read_csv('./tox21/tox21_dense_test.csv.gz', index_col=0, compression="gzip")
x_tr_sparse = io.mmread('./tox21/tox21_sparse_train.mtx.gz').tocsc()
x_te_sparse = io.mmread('./tox21/tox21_sparse_test.mtx.gz').tocsc()

print x_te_dense.shape
sparse_col_idx = ((x_tr_sparse > 0).mean(0) > 0.05).A.ravel()
#x_tr = np.hstack([x_tr_dense, x_tr_sparse[:, sparse_col_idx].A])
#x_te = np.hstack([x_te_dense, x_te_sparse[:, sparse_col_idx].A])

def add_name(x):
	return x+'-01'
test_index = pd.Series(test.index).apply(add_name)
print len(set(test_index).intersection(set(x_te_dense.index)))

"""
ms_raw = skchem.read_sdf(train)

pipeline = skchem.pipeline.Pipeline([skchem.filters.OrganicFilter(),
skchem.filters.MassFilter(above=100, below=1000),
skchem.filters.AtomNumberFilter(above=5, below=100),
skchem.descriptors.MorganFeaturizer()])

X, y = pipeline.transform_filter(ms_raw)

print X.shape

There are various types of input features 
such as physico-chemical descriptors, 
extended-connectivity fingerprints (ECFP) 
and other molecular descriptors that are typically used in that research areas.
Use rdkit and skchem python libraries
"""