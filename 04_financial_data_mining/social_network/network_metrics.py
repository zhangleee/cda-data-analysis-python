# -*- coding: utf-8 -*-
"""
补充 - 社交网络：核心度量指标

知识点说明：
度中心性、介数中心性、接近中心性等网络度量指标，识别关键节点。

本文件由CDA教材ipynb转换而来，补充了详细中文注释以帮助理解。
"""

import warnings
warnings.filterwarnings("ignore")

# --- 代码块 1 ---
##======================================================
##                        有向图                       ##
##======================================================

# --- 代码块 2 ---
#1.导入相应的包
import networkx as nx
import matplotlib.pyplot as plt

# --- 代码块 3 ---
##1.1添加无向图
##--定义无向图 
G = nx.Graph()

# --- 代码块 4 ---
##--定义图的节点
nodes=['1','2','3','4','5','6','7']

# --- 代码块 5 ---
##--增加图添加节点
G.add_nodes_from(nodes) 

nx.draw_networkx(G,node_color = 'g',with_labels = True,font_color='w',font_size =8,node_size =200)

plt.show()

# --- 代码块 6 ---
##--增加图边
edges=[('1','2',1),('1','6',1),('1','7',1),('2','3',1),('3','4',1),('4','5',1),('4','7',1),('5','6',1),('6','7',1),('7','5',1)]

# --- 代码块 7 ---
#定义有向图 
G = nx.DiGraph() 
#添加节点和边 
G.add_nodes_from(nodes) 
G.add_weighted_edges_from(edges) 
nx.draw_networkx(G,node_color = 'g',with_labels = True,font_color='w',font_size =8,node_size =200) #详细见draw_networkx介绍
plt.show()

# --- 代码块 8 ---
#度
nx.degree(G)

# --- 代码块 9 ---
#出度
G.out_degree(G)

# --- 代码块 10 ---
#入度
G.in_degree(G)

# --- 代码块 11 ---
##======================================================
##                        无向图                       ##
##======================================================

# --- 代码块 12 ---
#清除无向图 
G.clear()

# --- 代码块 13 ---
##1.1添加无向图
##--定义无向图 
G = nx.Graph()

# --- 代码块 14 ---
##--定义图的节点
nodes=['A','B','C','D','E','F']

# --- 代码块 15 ---
##--增加图添加节点
G.add_nodes_from(nodes) 

nx.draw_networkx(G,node_color = 'g',with_labels = True,font_color='w',font_size =8,node_size =200)

plt.show()

# --- 代码块 16 ---
##--增加图边
edges=[('A','B',1),('A','C',1),('A','D',1),('A','E',1),('A','F',1)]

# --- 代码块 17 ---
##--展示无向图
G.add_weighted_edges_from(edges) 
nx.draw_networkx(G,node_color = 'g',with_labels = True,font_color='w',font_size =8,node_size =200) #详细见draw_networkx介绍
plt.show()

# --- 代码块 18 ---
#指标1：度中心度  m/(n-1)
nx.degree_centrality(G)

# --- 代码块 19 ---
#指标2：紧密中心度
nx.closeness_centrality(G)

# --- 代码块 20 ---
#指标3：介度中心度
nx.betweenness_centrality(G)

# --- 代码块 21 ---
#指标4：特征向量中心度
nx.eigenvector_centrality(G)
