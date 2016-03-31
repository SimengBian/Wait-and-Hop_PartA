#coding=utf-8
'''
主函数，给定optimization interval（每隔多长时间进行一次优化），调用shuffleBytes函数，以及画图函数draw。
'''
from shuffleBytes import shuffleBytes
from drawPicture import draw

print "main begin:"

opt_len = -1 # optimization interval，表示每10s进行一次优化
total_time = shuffleBytes(opt_len) # shuffleBytes返回值为总的完成时间
print total_time # 打印总完成时间
draw(opt_len) # 画图

print "main end"
