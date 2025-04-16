# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 16:35:40 2025

@author: kunla1ve
"""

import numpy as np
import simpy

# 定义全局变量来存储统计数据
wait_times = []

# 定义M/M/c队列模型
def mmc_queue(env, arrival_rate, service_rate, num_servers):
    # 创建服务器资源
    server = simpy.Resource(env, capacity=num_servers)
    
    while True:
        # 生成到达间隔时间
        inter_arrival = np.random.exponential(1/arrival_rate)
        yield env.timeout(inter_arrival)
        
        # 处理每个到达的顾客
        env.process(customer(env, server, service_rate))

# 定义顾客行为
def customer(env, server, service_rate):
    # 记录顾客到达时间
    arrival_time = env.now
    
    # 请求服务器资源
    with server.request() as request:
        yield request
        
        # 计算等待时间并记录
        wait = env.now - arrival_time
        wait_times.append(wait)
        
        # 生成服务时间
        service_time = np.random.exponential(1/service_rate)
        yield env.timeout(service_time)

# 参数设置
arrival_rate = 2  # 到达率 λ
service_rate = 3  # 服务率 μ
num_servers = 2  # 服务器数量 c

# 创建环境和运行仿真
env = simpy.Environment()
env.process(mmc_queue(env, arrival_rate, service_rate, num_servers))
env.run(until=100000)

# 计算和输出性能指标
average_wait = np.mean(wait_times)
utilization = arrival_rate / (service_rate * num_servers)
print(f'平均等待时间: {average_wait}')
print(f'系统利用率: {utilization}')



