'''
This py file is used to generate the best vlan assignment according to present state
'''
import numpy as np
import math
import random
import time
from maxminRate import maxminRate
from getRoute import getRoute

def markov_byte_rndngb(tm):
	r1 = np.load("initialData/number.npz")
	numhost = r1["arr_0"]
	numvlan = r1["arr_3"]
	numhash = r1["arr_5"]
	r2 = np.load("initialData/matrices.npz")
	C = r2["arr_0"]
	r3 = np.load("initialData/p_matrices.npz")
	projMat = r3["arr_0"]

	#print "markov_byte_rndngb begin:"
	alpha = 1.0
	beta = 5.0
	maxT = 100
	active = tm > 0
	numcand = numvlan
	#history = np.zeros((maxT,1))

	x0 = np.arange(0,numhash,1)
	x0 = np.mod(x0,numvlan) # initial vlan assignment[0,1,2,3,0,1,2,3]
	x_now = x0.copy()
	dictionary = {}
	t = 0
	while t < maxT:
		R = getRoute(x_now,projMat)
		rate = maxminRate(active,R,C) # rate matrix at this initial condition,the entry in the rate matrix is the flow's rate
		#rate = calculateRate(active,R,C)
		f = np.sum(rate) # the sum of all the flow's rate,can be think as the throughtput
		test = np.dot(R,rate)
		Phit = test/C
		Phi = max(Phit)
		#print Phi
		countdown = np.zeros((numhash,1))
		for i in range(numhash):
			lamd = alpha * (numvlan-1) * math.exp(beta*Phi) /100.0
			ctime = np.random.exponential(lamd)
			countdown[i] = ctime
		mintime = np.amin(countdown)
		minclass = np.argmin(countdown)
		dictionary[x2string(x_now)] = dictionary.get(x2string(x_now),0) + mintime
		while 1:
			temp = np.random.randint(numvlan)
			if(temp!=x_now[minclass]):
				break
		x_now[minclass] = temp
		t = t + mintime

	x_best = string2x(findBest(dictionary))
	return x_best

def x2string(x):
	temp = []
	for i in range(len(x)):
		temp.append(str(x[i]))
	temp_str = ""
	temp_str = temp_str.join(temp)
	return temp_str

def string2x(s):
	temp = []
	for i in range(len(s)):
		temp.append(int(s[i]))
	return temp

def findBest(d):
	maxValue = 0
	for t in d.items():
		if t[1] > maxValue:
			maxStr = t[0]
			maxValue = t[1]
	return maxStr