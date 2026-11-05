# -*- coding: utf-8 -*-
"""
第7章 特征降维 - 主成分分析(PCA)

知识点说明：
主成分分析(PCA)通过线性变换将高维数据投影到低维空间，保留最大方差信息，是最常用的无监督降维方法。

本文件由CDA教材ipynb转换而来，补充了详细中文注释以帮助理解。
"""

import warnings
warnings.filterwarnings("ignore")


############################################################
# # 在 Python 中实现主成分分析.
# 一家电信运营商希望根据客户在几个主要业务上的使用情况，对客户进行分群
# 分析。
############################################################


############################################################
# ![image.png](attachment:image.png)
############################################################

# --- 代码块 3 ---
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- 代码块 4 ---
profile = pd.read_csv("profile_telecom.csv")
profile.head()

# --- 代码块 5 ---
data = profile.loc[:,"cnt_call":]
data.corr(method = "pearson")

# --- 代码块 6 ---
from sklearn.preprocessing import scale
from sklearn.decomposition import PCA
data_scaled = scale(data)
pca = PCA(n_components = 2, whiten = True).fit(data_scaled)
pca.explained_variance_ratio_

# --- 代码块 7 ---
pca.components_

# --- 代码块 8 ---
pca.transform(data_scaled)


############################################################
#
############################################################
