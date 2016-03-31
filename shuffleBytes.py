#coding=utf-8

import numpy as np

from markov_byte_rndngb import markov_byte_rndngb
from getRoute import getRoute
from maxminRate import maxminRate
from calculateRate import calculateRate


def shuffleBytes(opt_len):
	r1 = np.load("initialData/number.npz")
	numhost = r1["arr_0"]
	numhash = r1["arr_5"]
	r2 = np.load("initialData/matrices.npz")
	C = r2["arr_0"]
	r3 = np.load("initialData/p_matrices.npz")
	projMat = r3["arr_0"]
	TMvec = r3["arr_1"]

	# 这两个list分别保存的是时间点和对应的总吞吐量
	opt_time = [0.0]
	tot_thr = [0.0]
	length = numhash * numhost * numhost
	tm = np.reshape(TMvec.T,(length,1)).copy()
	#print tm
	total_T = 0.0 # return value
	#last_T = 0.0 
	next_opt_time = opt_len
	count = 0 # for debug

	vlan_assign = markov_byte_rndngb(tm)
	while 1:
		count = count + 1 # for debug
		if opt_len < 0:
			vlan_assign = markov_byte_rndngb(tm)
		elif total_T >= next_opt_time:
			vlan_assign = markov_byte_rndngb(tm)
			next_opt_time = next_opt_time + opt_len

		active = tm > 0

		R = getRoute(vlan_assign,projMat)
		rate = maxminRate(active, R, C)
		#rate = calculateRate(active, R, C)
		forDebug = np.sum(rate) # for debug
		
		#print np.sum(active)," flows left"

		inf = float("inf")
		duration = inf
		# find the flow's least finish time as duration
		for i in range(length):
			if tm[i] > 0.0:
				a = tm[i]
				b = rate[i]
				t = tm[i]/rate[i]
				if t < duration:
					duration = t
					need = i
		# duration is infinity means that all flows is done
		if duration == inf:
			break
		if opt_len > 0 and total_T+duration > next_opt_time:
			duration = next_opt_time - total_T
		total_T = total_T + duration
		for i in range(length):
			if tm[i] > 0.0:
				tm[i] = tm[i] - rate[i] * duration
				if tm[i] < 0.00000000000000000001:
					tm[i] = 0

		tot_thr.append(np.sum(rate)) # total throughtput
		opt_time.append(total_T) # time

	# save the result as txt file
	l = len(tot_thr)
	data = np.zeros((2,l))
	data[0] = opt_time
	data[1] = tot_thr
	if(opt_len < 0):
		np.savetxt("per_flow.txt",data,fmt = '%.6s')
	elif(opt_len == 1):
		np.savetxt("per_second.txt",data,fmt = '%.6s')
	elif(opt_len == 5):
		np.savetxt("per_5s.txt",data,fmt = '%.6s')
	elif(opt_len == 10):
		np.savetxt("per_10s.txt",data,fmt = '%.6s')
	else:
		# print "Please choose right optimization interval."
		np.savetxt("other.txt",data,fmt = '%.6s')
	# print count
	return total_T


