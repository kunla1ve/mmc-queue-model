# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 20:22:34 2025

@author: kunla1ve
"""

import numpy as np
import heapq
from collections import deque

class HyperExponentialServer:
    def __init__(self, rates, probs):
        """
        超指数分布服务时间生成器
        :param rates: 各指数分布的速率列表 [μ1, μ2, ...]
        :param probs: 选择各分布的概率列表 [p1, p2, ...] (需sum=1)
        """
        self.rates = rates
        self.probs = probs
        assert np.isclose(sum(probs), 1.0), "Probabilities must sum to 1"
    
    def generate_service_time(self):
        """生成服从超指数分布的服务时间"""
        chosen_dist = np.random.choice(len(self.rates), p=self.probs)
        return np.random.exponential(1/self.rates[chosen_dist])

class MHyperExponentialNQueue:
    def __init__(self, arrival_rate, n_servers, hyperexp_params, sim_time):
        """
        M/HyperExponential/n 排队系统仿真
        :param arrival_rate: 到达率 λ
        :param n_servers: 服务台数量 n
        :param hyperexp_params: 超指数参数 (rates, probs)
        :param sim_time: 仿真时间
        """
        self.arrival_rate = arrival_rate
        self.n_servers = n_servers
        self.sim_time = sim_time
        
        # 初始化超指数服务时间生成器
        self.service_dist = HyperExponentialServer(*hyperexp_params)
        
        # 系统状态
        self.queue = deque()
        self.servers_busy = 0  # 记录忙碌服务器数量
        self.busy_time = 0.0    # 累计所有服务器的忙碌时间
        self.event_queue = []
        
        # 统计数据
        self.total_customers = 0
        self.total_wait_time = 0.0    # 总等待时间(队列中)
        self.total_service_time = 0.0  # 总服务时间
        self.total_queue_length = 0.0  # 队列长度积分
        self.total_system_customers = 0.0  # 系统中顾客数积分
        self.time_last_event = 0.0
        
    def schedule_event(self, event_time, event_type):
        """调度事件"""
        heapq.heappush(self.event_queue, (event_time, event_type))
    
    def run_simulation(self):
        """运行仿真"""
        # 初始化第一个到达事件
        first_arrival = np.random.exponential(1/self.arrival_rate)
        self.schedule_event(first_arrival, 'arrival')
        
        current_time = 0.0
        
        while current_time < self.sim_time and self.event_queue:
            current_time, event_type = heapq.heappop(self.event_queue)
            
            # 更新统计信息
            time_elapsed = current_time - self.time_last_event
            self.total_queue_length += len(self.queue) * time_elapsed
            self.total_system_customers += (len(self.queue) + self.servers_busy) * time_elapsed
            self.busy_time += self.servers_busy * time_elapsed
            self.time_last_event = current_time
            
            if event_type == 'arrival':
                self.handle_arrival(current_time)
            elif event_type == 'departure':
                self.handle_departure(current_time)
        
        # 计算性能指标
        if self.total_customers == 0:
            return {
                'Lq': 0,  # 平均等待队列长度
                'Ls': 0,  # 系统中平均顾客数
                'Wq': 0,  # 平均等待时间
                'Ws': 0,  # 系统中平均逗留时间
                'utilization': 0,  # 服务台利用率
                'total_customers': 0
            }
            
        avg_queue_length = self.total_queue_length / current_time  # Lq
        avg_system_customers = self.total_system_customers / current_time  # Ls
        avg_wait_time = self.total_wait_time / self.total_customers  # Wq
        avg_system_time = (self.total_wait_time + self.total_service_time) / self.total_customers  # Ws
        server_utilization = self.busy_time / (current_time * self.n_servers)
        
        return {
            'Lq': avg_queue_length,
            'Ls': avg_system_customers,
            'Wq': avg_wait_time,
            'Ws': avg_system_time,
            'utilization': server_utilization,
            'total_customers': self.total_customers
        }
    
    def handle_arrival(self, current_time):
        """处理到达事件"""
        self.total_customers += 1
        
        # 安排下一个到达
        next_arrival = current_time + np.random.exponential(1/self.arrival_rate)
        if next_arrival < self.sim_time:
            self.schedule_event(next_arrival, 'arrival')
        
        # 如果有空闲服务器，立即服务
        if self.servers_busy < self.n_servers:
            self.servers_busy += 1
            service_time = self.service_dist.generate_service_time()
            departure_time = current_time + service_time
            self.schedule_event(departure_time, 'departure')
            self.total_service_time += service_time
        else:
            # 否则加入队列
            self.queue.append(current_time)
    
    def handle_departure(self, current_time):
        """处理离开事件"""
        self.servers_busy -= 1
        
        # 如果队列不为空，服务下一个顾客
        if self.queue:
            arrival_time = self.queue.popleft()
            wait_time = current_time - arrival_time
            self.total_wait_time += wait_time
            
            service_time = self.service_dist.generate_service_time()
            departure_time = current_time + service_time
            self.schedule_event(departure_time, 'departure')
            self.servers_busy += 1
            self.total_service_time += service_time

# 示例使用
if __name__ == "__main__":
    # 参数设置
    arrival_rate = 2       # 到达率 λ
    n_servers = 2            # 服务台数量
    sim_time = 1000000         # 仿真时间
    
    # 超指数分布参数 (两个指数分布的混合)
    # 均值相同但方差更大
    mu1, mu2 = 1.5, 2.5      # 两个服务率
    p1, p2 = 0.5, 0.5        # 混合概率
    
    # 运行仿真
    queue = MHyperExponentialNQueue(
        arrival_rate=arrival_rate,
        n_servers=n_servers,
        hyperexp_params=([mu1, mu2], [p1, p2]),
        sim_time=sim_time
    )
    
    results = queue.run_simulation()
    
    # 打印结果
    print("M/HyperExponential/n 排队系统仿真结果:")
    print(f"平均等待队列长度 (Lq): {results['Lq']:.4f}")
    print(f"系统中平均顾客数 (Ls): {results['Ls']:.4f}")
    print(f"平均等待时间 (Wq): {results['Wq']:.4f}")
    print(f"系统中平均逗留时间 (Ws): {results['Ws']:.4f}")
    print(f"服务台利用率: {results['utilization']:.4f}")
    print(f"处理的顾客总数: {results['total_customers']}")
    
    
    
    
    
    # M/HyperExponential/n 排队系统仿真结果:
    # 平均等待队列长度 (Lq): 0.4468
    # 系统中平均顾客数 (Ls): 1.5136
    # 平均等待时间 (Wq): 0.2236
    # 系统中平均逗留时间 (Ws): 0.7574
    # 服务台利用率: 0.5334
    # 处理的顾客总数: 1998496
    
    
    
    