'''
This py file is used to allocate flow.
active is an 0-1 array that indicate this flow is 0 or not.
R is the routing matrix which stores the shortest path information.
C is the capacity matrix.
The return value of this function is a rate matrix,whose entry is the rate this flow can be allocated under this situation. 
'''
from getRoute import getRoute
import numpy as np

def maxminRate(active,R,C):

	inf = float("inf")
	hostRate = 0.001
	L = len(C) # length of link(20)
	#print L
	F = len(active) # length of flow(128)
	#print F

	C_res = C.copy()
	# active is active matrix 0-1 128*1
	f = active.copy()
	rate = np.zeros((F,1))

	while(np.sum(f) >= 1): # if there is still some flow not allocated
		#print "sum(f):"
		#print sum(f)
		fcount = np.dot(R,f) # fcount is a matrix that show the number of flows that this link will transport.
		#print "fcount:"
		#print fcount

		fshare = inf * np.ones((L,1))
		for l in range(L):
			if fcount[l] > 0:
				fshare[l] = C_res[l] / fcount[l] # fshare[l] is the "share" that all flows that will use link l can get
		# minlink is the bottleneck link
		minlink = np.argmin(fshare)
		# val is the minimum share
		val = np.amin(fshare)
		#print "minlink:"
		#print minlink

		# Allocate flow,every flow get some rate allocated
		for i in range(F):
			if(R[minlink][i] == 1 and f[i] > 0):
				rate[i] = min(rate[i] + val,hostRate)
				#rate[i] = rate[i] + val
				f[i] = 0

		C_res = C - np.dot(R,rate)
	#print "maactiveminRate end"
	return rate
	

if __name__ == '__main__':
	active = np.ones((128,1))
	for i in range(128):
		if i%4 == 0:
			active[i] = 0
	vlan_assign = [0,1,2,3,0,1,2,3]
	r3 = np.load("initialData/p_matrices.npz")
	projMat = r3["arr_0"]
	r2 = np.load("initialData/matrices.npz")
	C = r2["arr_0"]
	R = getRoute(vlan_assign,projMat)
	r = maxminRate(active,R,C)
	print sum(r)