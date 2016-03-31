'''
This py file is used to build the essential topology information.
And all the variables' meaning are in my documentation.
'''
import numpy as np

numhost = 4
numsw = numhost
numhash = 8
N = numhost + numsw

# Adjacent matrix
Adj = np.zeros((N, N), dtype=int)
N2L = np.zeros((N, N), dtype=int)
# L2N = np.zeros((N*N,2),dtype=int)
idx = 0
for h in range(numhost):
    sw = h + numhost
    Adj[h][sw] = 1
    Adj[sw][h] = 1

    N2L[h][sw] = idx
    N2L[sw][h] = idx + 1

    idx = idx + 2

for s1 in range(numhost, N):
    for s2 in range(s1 + 1, N):
        Adj[s1][s2] = 1
        Adj[s2][s1] = 1

        N2L[s1][s2] = idx
        N2L[s2][s1] = idx + 1

        idx = idx + 2

# Capacity matrix	
numlink = np.sum(Adj) / 2
C = np.zeros((2 * numlink, 1))
idx = 0
for i in range(numhost):
    C[idx] = 1
    C[idx + 1] = 1
    idx += 2
for j in range(numhost, numlink):
    C[idx] = 0.01
    C[idx + 1] = 0.01
    idx += 2
# for i in range(numhost):
#     C[idx] = 0.01
#     C[idx + 1] = 0.01
#     idx += 2
# for j in range(numhost, numlink):
#     C[idx] = 1
#     C[idx + 1] = 1
#     idx += 2

# VLAN matrix
numvlan = numsw
VLAN = [np.zeros((N, N)) for r in range(numvlan)]
for v in range(numvlan):
    for i in range(numhost):
        VLAN[v][i][i + numhost] = 1
        VLAN[v][i + numhost][i] = 1
    for i in range(numsw):
        if i == v:
            continue
        VLAN[v][v + numhost][i + numhost] = 1
        VLAN[v][i + numhost][v + numhost] = 1

# Traffic Matrix
TM = [np.zeros((numhost, numhost)) for r in range(numhash)]
for h in range(numhash):
    for i in range(numhost):
        for j in range(numhost):
            if i == j:
                TM[h][i][j] = 0
            else:
                TM[h][i][j] = 0.1

np.savez("initialData/matrices.npz",C,Adj,N2L,VLAN,TM)
np.savez("initialData/number.npz",numhost,numsw,N,numvlan,numlink,numhash)
