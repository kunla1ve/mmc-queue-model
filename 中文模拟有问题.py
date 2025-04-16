# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 16:27:00 2025

@author: kunla1ve
"""

import numpy as np

# 参数设置
lambda_rate = 2  # 客户到达率（每小时）
mu_rate = 3       # 每个窗口的服务率（每小时）
c = 2             # 服务窗口数量
total_hours = 100   # 总模拟时间（小时）

# 初始化
current_time = 0
queue = [] # 队列，用于存储客户到达的时间
service_times = [float('inf')] * c # 每个窗口的服务完成时间

waiting_times = []

# 模拟过程
while current_time < total_hours:
    arrival_time = current_time + np.random.exponential(1/lambda_rate) # 下一个客户到达的时间
    next_service_time = min(service_times) # 下一个服务完成的时间
    next_event_time = min(arrival_time, next_service_time)

    # 如果客户先到达
    if arrival_time <= next_service_time:
        current_time = arrival_time
        queue.append(current_time) # 客户加入队列
        if len(queue) <= c:
            # 如果有空闲窗口，则开始服务
            service_index = len(queue) - 1
            service_times[service_index] = current_time + np.random.exponential(1/mu_rate)
    else:
        # 如果服务先完成
        current_time = next_service_time
        finished_service_index = service_times.index(next_service_time)
        arrival_time_of_served_customer = queue.pop(0) # 服务完成的客户离开队列
        waiting_time = current_time - arrival_time_of_served_customer # 计算等待时间
        if len(queue) >= c:
            # 如果队列中有更多客户等待，则开始为下一个客户提供服务
            service_times[finished_service_index] = current_time + np.random.exponential(1/mu_rate)
        else:
            service_times[finished_service_index] = float('inf')
        waiting_times.append(waiting_time)

# 计算平均等待时间
average_waiting_time = np.mean(waiting_times)
print("平均等待时间（小时）：", average_waiting_time)