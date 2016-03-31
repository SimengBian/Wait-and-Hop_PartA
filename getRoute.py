'''
given a vlan assignment and the projMat,return R
see the documentation for more details
'''
import numpy as np

def getRoute(x,projMat):
	#print "getRoute begin:"
	r1 = np.load("initialData/number.npz")
	numhost = r1["arr_0"]
	numlink = r1["arr_4"]
	numhash = len(x)
	numvlan = len(projMat)
	numhost2 = numhost * numhost
	R = np.zeros((2*numlink,numhash*numhost2))
	for h in range(numhash):
		v = x[h]
		R[::1,h*numhost2:h*numhost2+numhost2] = projMat[v]
		# for i in range(2*numlink):
		# 	for j in range(numhost2):
		# 		R[i][h*numhost2+j] = projMat[v][i][j]

	#print "getRoute end"
	return R

	