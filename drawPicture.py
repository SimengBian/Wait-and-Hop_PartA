#coding=utf-8
'''
画图函数，将程序运行后得到的数据作图呈现出来
'''
import matplotlib.pyplot as plt

def draw(opt_len):
	filename = "" # 所要读取的结果数据文件的名称，根据opt_len的不同而不同
	if(opt_len < 0):
		filename = "per_flow"
	elif(opt_len == 1):
		filename = "per_second"
	elif(opt_len == 5):
		filename = "per_5s"
	elif(opt_len == 10):
		filename = "per_10s"
	else:
		filename = "other"
	f = open(filename + ".txt","r")
	line1 = f.readline()
	line2 = f.readline()
	x = line1.split()
	y = line2.split()
	y[0] = y[1]
	for i in range(len(y)):
		y[i] = 100* float(y[i])
	plt.figure(figsize=(10,5), dpi=80)
	#plt.xlable("Time") # 设置xlable，ylable老是报错，暂时注释掉
	# plt.ylable("Total Throughput")
	plt.plot(x,y,"o-",color= 'r')
	f.close()
	plt.ylim(0,12)
	plt.savefig(filename+".eps")
	plt.show()

'''
这部分可用于调试
'''
if __name__ == '__main__':
 	draw(5)