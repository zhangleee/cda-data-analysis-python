# -*- coding: utf-8 -*-
"""
补充 - 社交网络：综合小案例

知识点说明：
社交网络分析综合案例：从数据构建到指标计算与可视化。

本文件由CDA教材ipynb转换而来，补充了详细中文注释以帮助理解。
"""

import warnings
warnings.filterwarnings("ignore")


############################################################
# ### 社交网络分析
############################################################


############################################################
# #### 社交网络算法-小案例
#
# ##导入相关的包
############################################################

# --- 代码块 3 ---
import networkx as nx  
import pandas as pd
import matplotlib.pyplot as plt

# --- 代码块 4 ---
#nx.test()

# --- 代码块 5 ---
edge_list=pd.read_csv('./data/stormofswords.csv')
edge_list.head()

# --- 代码块 6 ---
edge_list.Weight=edge_list.Weight.astype(int)

# --- 代码块 7 ---
#edge_list

# --- 代码块 8 ---
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
        node_size =20)
    plt.show()

# --- 代码块 9 ---
plot_network(edge_list)
