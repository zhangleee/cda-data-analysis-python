# -*- coding: utf-8 -*-
"""
补充 - 社交网络：PageRank算法

知识点说明：
PageRank算法原理与手动实现，用于衡量节点在网络中的重要性。

本文件由CDA教材ipynb转换而来，补充了详细中文注释以帮助理解。
"""

import warnings
warnings.filterwarnings("ignore")

# --- 代码块 1 ---
#PageRank-Python实现

# --- 代码块 2 ---
import numpy as np
import random

# --- 代码块 3 ---
#############################################
#############################################
#########  第一部分：简单测试
#############################################
#############################################

# --- 代码块 4 ---
#以不本篇简单例子为例
#初始矩阵M

# --- 代码块 5 ---
M =np.array([[0,1/2,0,1/2],
   [1/3,0,0,1/3],
   [1/3,1/2,0,0],
   [1/3,0,1,0]])

# --- 代码块 6 ---
M

# --- 代码块 7 ---
v =np.array( [[1/4],[1/4],[1/4],[1/4]])

# --- 代码块 8 ---
v

# --- 代码块 9 ---
Mv1 = np.dot(M,v)

# --- 代码块 10 ---
Mv1

# --- 代码块 11 ---
def MV_computer(N):
    for i in range(N):
        Mv = np.dot(M,v)
        i = i+1   
    return Mv

# --- 代码块 12 ---
Result = MV_computer(1000)

# --- 代码块 13 ---
Result

# --- 代码块 14 ---
#############################################
#############################################
#########  第二部分：随机测试
#############################################
#############################################

# --- 代码块 15 ---
def PR_Gdata(N, alpha=0.8): # random > alpha, then here is a edge.
    G = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            if random.random() < alpha:
                G[i][j] = 1
    return G
G1 = PR_Gdata(10)

# --- 代码块 16 ---
G1

# --- 代码块 17 ---
def pagerank_GtoM(G1, N):
    M = np.zeros((N, N))
    for i in range(N):
        D_i = sum(G1[i])
        if D_i == 0:
            continue
        for j in range(N):
            M[j][i] = G1[i][j] / D_i # 边和链接矩阵转换
    return M
M1 = pagerank_GtoM(G1, 10)

# --- 代码块 18 ---
def PageRank(M, N, T=300, eps=1e-6):
    R = np.ones(N) / N
    for time in range(T):
        R_new = np.dot(M, R)
        if np.linalg.norm(R_new - R) < eps:
            break
        R = R_new.copy()
    return R_new

# --- 代码块 19 ---
Result = PageRank(M=M1,N=10)

# --- 代码块 20 ---
Result = PageRank(M,4,T=300, eps=1e-6)

# --- 代码块 21 ---
Result
