# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 16:42:16 2025

@author: kunla1ve
"""



import numpy as np
import matplotlib.pyplot as plt
import math  # 导入标准库中的 math 模块
from IPython.display import display, Math


def mmc_queue(lam, mu, s, n_max):
    """
    计算M/M/c队列模型的稳态概率 Pn 及相关性能指标
    :param lam: 平均到达率 (mean arrival rate)
    :param mu: 平均服务率 (mean service rate)
    :param s: 服务器数量 (number of servers)
    :param n_max: 最大顾客数量 (maximum number of customers to consider)
    :return: Pn (稳态概率), Lq (平均等待队列长度), Ls (系统中平均顾客数), Wq (平均等待时间), Ws (系统中平均逗留时间)
    """
    rho = lam / (s * mu)  # 系统流量强度 (traffic intensity)
    
    if rho >= 1:
        raise ValueError("系统不稳定 (rho >= 1)。")
    
    # 计算 P0
    
    #系统中顾客数少于服务器数量时的概率
    display(Math(r'P_{\text{less\_than\_s}} = \sum_{k=0}^{s-1} \frac{(s \rho)^k}{k!}'))
    prob_less_than_s = sum([(s * rho) ** k / math.factorial(k) for k in range(s)])  # 使用 math.factorial

    # 系统中顾客数大于或等于服务器数量时的概率
    display(Math(r'P_{\text{greater\_or\_equal\_s}} = \frac{(s \rho)^s}{s! (1 - \rho)}'))
    prob_greater_or_equal_s = (s * rho) ** s / (math.factorial(s) * (1 - rho))
    
    
    P0 = 1 / (prob_less_than_s + prob_greater_or_equal_s)  # 使用 math.factorial
    
    
    # 计算 Pn
    Pn = []
    for n in range(n_max + 1):
        if n <= s:
            Pn.append((lam / mu) ** n / math.factorial(n) * P0)  # 使用 math.factorial
        else:
            Pn.append((lam / mu) ** n / (math.factorial(s) * s ** (n - s)) * P0)  # 使用 math.factorial
    
    # 计算 Lq (平均等待队列长度)
    Lq = (P0 * (s * rho) ** s * rho) / (math.factorial(s) * (1 - rho) ** 2)  # 使用 math.factorial
    # 计算 Ls (系统中平均顾客数)
    Ls = Lq + (lam / mu)
    # 计算 Wq (平均等待时间)    Little's Law
    Wq = Lq / lam
    # 计算 Ws (系统中平均逗留时间)
    Ws = Wq + (1 / mu)
    
    return Pn, Lq, Ls, Wq, Ws

# 参数设置
lam = 2  # 平均到达率 (mean arrival rate)
mu = 2   # 平均服务率 (mean service rate)
s = 2      # 服务器数量 (number of servers)
n_max = 10 # 显示的顾客数量 (Number of customers displayed)

# 计算 Pn 及相关性能指标
Pn, Lq, Ls, Wq, Ws = mmc_queue(lam, mu, s, n_max)

# 输出性能指标
print(f"平均等待队列长度 (Lq): {Lq:.4f}")
print(f"系统中平均顾客数 (Ls): {Ls:.4f}")
print(f"平均等待时间 (Wq): {Wq:.4f}")
print(f"系统中平均逗留时间 (Ws): {Ws:.4f}")

# # 绘制柱状图
# n_values = np.arange(0, n_max + 1)
# plt.bar(n_values, Pn, color='blue', alpha=0.7)
# plt.xlabel('Number of customers (n)')
# plt.ylabel('Probability (Pn)')
# plt.title('M/M/c Queue: Pn vs Probability')
# plt.xticks(n_values)
# plt.grid(True, axis='y', linestyle='--', alpha=0.7)
# plt.show()
