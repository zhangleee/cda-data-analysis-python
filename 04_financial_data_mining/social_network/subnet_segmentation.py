# -*- coding: utf-8 -*-
"""
补充 - 社交网络：子网分割案例

知识点说明：
使用社区发现算法进行子网分割，识别网络中的紧密群体。

本文件由CDA教材ipynb转换而来，补充了详细中文注释以帮助理解。
"""

import warnings
warnings.filterwarnings("ignore")

# --- 代码块 1 ---
import networkx as nx  
import pandas as pd
import matplotlib.pyplot as plt

edge_list=pd.read_csv(r".\data\stormofswords.csv")

edge_list.head()

edge_list.Weight=edge_list.Weight.astype(int)


def plot_network(pd_table):
    '''
    绘制网络关系图
    '''
    G = nx.from_pandas_edgelist(edge_list, source = 'Source', target = 'Target', 
                                edge_attr = 'Weight',create_using = nx.DiGraph())
    nx.draw(G,
        #pos = nx.spiral_layout(G),
        node_color = 'b', 
        edge_color = 'r',
        with_labels = True,
        font_size =10,
        node_size =200,)
    plt.show()

# --- 代码块 2 ---
plot_network(edge_list)

# --- 代码块 3 ---
G=nx.from_pandas_edgelist(edge_list,'Source',"Target",edge_attr=True)

# --- 代码块 4 ---
import networkx as nx
import community
#from community import  community_louvain

# --- 代码块 5 ---
partition = community.best_partition(G)

# --- 代码块 6 ---
partition

# --- 代码块 7 ---
len(partition)

# --- 代码块 8 ---
len(set(partition.values()))

# --- 代码块 9 ---
import community as community_louvain
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import networkx as nx

# --- 代码块 10 ---
pos = nx.spring_layout(G)
# color the nodes according to their partition
cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
nx.draw_networkx_nodes(G, pos, partition.keys(), node_size=40,
                       cmap=cmap, node_color=list(partition.values()))
nx.draw_networkx_edges(G, pos, alpha=0.5)
plt.show()
