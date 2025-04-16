# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 16:11:40 2025

@author: kunla1ve
"""

import argparse

# 创建参数解析器
parser = argparse.ArgumentParser()

# 添加参数
# --simT: 模拟时间，默认为2000
parser.add_argument('--simT', type=int, default=2000)
# --arrR: 到达率，默认为5
parser.add_argument('--arrR', type=int, default=5)
# --serR: 服务率，默认为3
parser.add_argument('--serR', type=int, default=3)
# --k: 服务器数量，默认为2
parser.add_argument('--k', type=int, default=2)

# 解析参数
args = parser.parse_args()

import random
import math
import copy
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

# 初始化列表
arrivalList = []  # 到达时间列表
serviceList = []  # 服务时间列表
startList = []  # 服务开始时间列表
departureList = []  # 离开时间列表
serverList = []  # 记录忙碌的服务器的离开时间

# 生成到达时间列表（独立）
arrivalTime = 0
while arrivalTime < args.simT:
    arrivalTime += random.expovariate(args.arrR)  # 使用指数分布生成到达时间
    arrivalList.append(arrivalTime)

'''
显示到达时间列表
'''
printArrivalList = [round(a, 3) for a in arrivalList]  # 对到达时间进行四舍五入
# print(printArrivalList)
aList = copy.copy(arrivalList)  # 复制到达时间列表

# 运行模拟
currentTime = 0
while currentTime < args.simT:

    currentTime = aList[0]  # 当前时间参考点

    # 如果服务器有空闲，则立即开始服务
    if len(serverList) < args.k:
        startTime = aList[0]
    else:
        # 否则，等待最早结束服务的服务器
        startTime = serverList[serverList.index(min(serverList))]
        del(serverList[serverList.index(min(serverList))])
    
    startList.append(startTime)  # 记录服务开始时间
    
    serviceTime = random.expovariate(args.serR)  # 生成服务时间
    serviceList.append(serviceTime)  # 记录服务时间

    departureTime = startTime + serviceTime  # 计算离开时间

    departureList.append(departureTime)  # 记录离开时间
    serverList.append(departureTime)  # 更新服务器的离开时间
    aList.pop(0)  # 移除已处理的到达时间

    if len(aList) == 0: break  # 如果到达时间列表为空，则结束模拟

    # 清理已完成服务的服务器
    while len(serverList) > 0:
        if serverList[serverList.index(min(serverList))] < aList[0]:
            del(serverList[serverList.index(min(serverList))])
        else: break
    
'''
性能评估
'''
waitList = [startList[i] - arrivalList[i] for i in range(len(startList))]  # 计算等待时间

# [1] 绘制等待时间直方图
# [2] 绘制服务时间直方图
bins = np.linspace(0, max(serviceList), 11)  # 设置直方图的区间

plt.hist(waitList, bins ,facecolor='red', alpha=0.5,label='Waiting Time (Counts)')  # 绘制等待时间直方图
arr=plt.hist(waitList, bins, facecolor='red', alpha=0.5)
for i in range(10):
    plt.text(arr[1][i], arr[0][i]+100, str(int(arr[0][i])),color='red')  # 在直方图上标注数值

plt.hist(serviceList, bins, facecolor='green', alpha=0.5,label='Service Time (Counts')  # 绘制服务时间直方图
arr=plt.hist(serviceList, bins, facecolor='green', alpha=0.5)
for i in range(10):
    plt.text(arr[1][i], arr[0][i]+100, str(int(arr[0][i])),color='green')  # 在直方图上标注数值

plt.xlabel('Service Time')  # 设置x轴标签
plt.ylabel('Counts')  # 设置y轴标签
plt.title('Counts of Waiting & Service Time for {} Patients in {} Minutes'.format(len(waitList), args.simT))  # 设置图表标题
plt.axis([min(serviceList), max(serviceList),0,len(serviceList)])  # 设置坐标轴范围
plt.grid(True)  # 显示网格
plt.legend(loc='upper right')  # 显示图例
plt.show()  # 显示图表

# 计算平均等待时间、平均服务时间、平均系统时间和平均系统中的顾客数
avgWait = sum(waitList)/len(waitList)
avgService = sum(serviceList)/len(serviceList)
avgTime = avgWait + avgService
avgCustomer_inSys = avgTime * args.arrR

# 计算系统利用率
rho = args.arrR / (args.k * args.serR)

'''
验证期望等待时间
'''
p1 = 0 
for n in range(args.k):
    p1 += (args.k*rho)**n / math.factorial(n)
p2 = (args.k*rho)**args.k / (math.factorial(args.k)*(1-rho))
p0 = 1 / (p1 + p2)
expectWait = ((args.arrR/args.serR)**args.k * args.serR / (math.factorial(args.k-1)*(args.k*args.serR - args.arrR)**2))*p0
expectTime = expectWait + 1/args.serR
expectCustomer_inSys = expectTime * args.arrR

# expWait_v1 = ((args.arrR/args.serR)**args.k / (math.factorial(args.k)*(args.k*args.serR)*(1-args.arrR/(args.k*args.serR))**2))*p0

# 输出结果
print(round(avgWait,5),'[average wait]')  # 输出平均等待时间
print(round(expectWait,5),'[expect wait]')  # 输出期望等待时间
print(round(avgCustomer_inSys, 3),'[average customer in system]')  # 输出平均系统中的顾客数
print(round(expectCustomer_inSys, 3),'[expect customer in system]')  # 输出期望系统中的顾客数