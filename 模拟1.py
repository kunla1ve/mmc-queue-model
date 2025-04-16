"""
Created on Wed Mar 12 20:23:46 2025
@author: kunla1ve
"""




import numpy as np
import simpy
import matplotlib.pyplot as plt

# 设置随机数种子以确保结果可重复
np.random.seed(42)

# 定义全局变量来存储统计数据
wait_times = []
system_customer_counts = []  # 记录系统中顾客数量的分布
service_times = []  # 记录每个顾客的服务时间

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
        # 生成服务时间 服务时间服从指数分布
        service_time = np.random.exponential(1 / service_rate)
        service_times.append(service_time)
        yield env.timeout(service_time)



# 定义M/M/c队列模型
def mmc_queue(env, arrival_rate, service_rate, server):
    while True:
        # 生成到达间隔时间  到达间隔时间应该服从指数分布
        inter_arrival = np.random.exponential(1 / arrival_rate)
        yield env.timeout(inter_arrival)
        # 处理每个到达的顾客
        env.process(customer(env, server, service_rate))



# 记录系统中顾客数量的分布
def monitor_system(env, server):
    while True:
        # 当前系统中的顾客数量 = 队列中的顾客数量 + 正在被服务的顾客数量
        system_customer_counts.append(len(server.queue) + len(server.users))
        yield env.timeout(0.1)  # 每隔0.1个时间单位记录一次

# 参数设置
arrival_rate = 5  # 到达率 λ
service_rate = 3  # 服务率 μ
num_servers = 2  # 服务器数量 c
simulation_time = 10000  # 仿真时间

# 创建环境
env = simpy.Environment()
# 运行仿真
server = simpy.Resource(env, capacity=num_servers)
#调用函数
env.process(mmc_queue(env, arrival_rate, service_rate, server))
env.process(monitor_system(env, server))
env.run(until=simulation_time)

# 计算性能指标
average_wait = np.mean(wait_times)
average_service_time = np.mean(service_times)
utilization = arrival_rate / (service_rate * num_servers)

# 计算平均等待队列长度 (Lq)
Lq = np.mean([max(0, count - num_servers) for count in system_customer_counts])

# 计算系统中平均顾客数 (Ls)
Ls = np.mean(system_customer_counts)

# 计算平均等待时间 (Wq)
Wq = np.mean(wait_times)

# 计算系统中平均逗留时间 (Ws)
Ws = Wq + average_service_time

# 输出性能指标
print(f"平均等待队列长度 (Lq): {Lq:.4f}")
print(f"系统中平均顾客数 (Ls): {Ls:.4f}")
print(f"平均等待时间 (Wq): {Wq:.4f}")
print(f"系统中平均逗留时间 (Ws): {Ws:.4f}")
print(f"系统利用率: {utilization:.4f}")

# 计算稳态概率 Pn
max_customers = max(system_customer_counts)
Pn = [system_customer_counts.count(n) / len(system_customer_counts) for n in range(max_customers + 1)]

# # 输出稳态概率 Pn
# for n, p in enumerate(Pn):
#     print(f"P{n}: {p:.4f}")

# 绘制稳态概率的柱状图
plt.bar(range(len(Pn)), Pn, color='blue')
plt.xlabel('Number of Customers (n)')
plt.ylabel('Probability Pn')
plt.title('Steady-State Probability Pn (Simulation)')
plt.show()

