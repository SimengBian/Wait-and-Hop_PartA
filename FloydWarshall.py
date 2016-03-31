'''
This py file is used to find the shortest path between two nodes.
'''
import numpy as np

r1 = np.load("initialData/number.npz")
numhost = r1["arr_0"]
N = r1["arr_2"]
numlink = r1["arr_4"]
r2 = np.load("initialData/matrices.npz")
N2L = r2["arr_2"]

inf = float("inf")
# given a adjacency matrix,return a "next" matrix.Each entry in "next" is the shortest path's next node id from node i to node j.
def floyd(G):
	path = G.copy()
	for i in range(N):
		for j in range(N):
			if(i==j):
				path[i][j] = 0
			elif(G[i][j] == 0):
				path[i][j] = inf

	next = -1 * np.ones((N,N))
	for i in range(N):
		for j in range(N):
			if (path[i][j] < inf):
				next[i][j] = 0

	for k in range(N):
		for i in range(N):
			for j in range(N):
				if(path[i][k] + path[k][j] < path[i][j]):
					path[i][j] = path[i][k] + path[k][j]
					next[i][j] = k

	return next


# give "next" and node x node y,return the shortest path from x to y
def getPath(n,x,y):
	out = []
	if(x == y):
		return out

	k = n[x][y]
	if(k == -1):
		out = []
	elif(k == 0):
		out = [x,y]
	else:
		out1 = getPath(n,x,k)
		out2 = getPath(n,k,y)
		out = out1 + out2
	return out

# given "next",return a matrix out whose entry is 1 means that the shortest path from node i to node j travels this specific link.
# see my documentation to know the detailed structure. 
def getAll(n):
	out = np.zeros((2 * numlink,numhost * numhost))
	for n1 in range(numhost):
		for n2 in range(numhost):
			col = n1 * numhost + n2
			nodepath = getPath(n,n1,n2)
			l = len(nodepath)
			for i in range(l/2):
				link = N2L[nodepath[2*i]][nodepath[2*i+1]]
				out[link][col] = 1
	return out
