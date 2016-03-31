'''
This py file is used to build projMat and TMvec.
'''
import numpy as np
from FloydWarshall import floyd
from FloydWarshall import getAll


r1 = np.load("initialData/number.npz")
numhost = r1["arr_0"]
numvlan = r1["arr_3"]
numlink = r1["arr_4"]
numhash = r1["arr_5"]

r2 = np.load("initialData/matrices.npz")
Adj = r2["arr_1"]
VLAN = r2["arr_3"]
TM = r2["arr_4"]
# print r2["arr_0"]

projMat = [np.zeros((2*numlink,numhost*numhost)) for r in range(numvlan)]
for v in range(numvlan):
	next = floyd(VLAN[v])
	projMat[v] = getAll(next)

TMvec_t = np.zeros((numhash,numhost*numhost))
for h in range(numhash):
	tm = TM[h]
	TMvec_t[h] = np.reshape(tm,numhost*numhost,1)

TMvec = TMvec_t.transpose()


np.savez("initialData/p_matrices.npz",projMat,TMvec)