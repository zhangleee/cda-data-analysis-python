# -*- coding: utf-8 -*-
"""
第9章 用户分群 - 层次聚类

知识点说明：
层次聚类通过构建树状图（谱系图）展示样本间的层级关系，不需要预先指定簇数，适合探索性分析。

本文件由CDA教材ipynb转换而来，补充了详细中文注释以帮助理解。
"""

import warnings
warnings.filterwarnings("ignore")

# --- 代码块 1 ---
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

# --- 代码块 2 ---
# 读取city10.csv该数据代码
#你的代码
df=pd.read_csv("cities_10.csv",encoding="gbk")
df

# --- 代码块 3 ---
#选取要用的特征
#你的代码
model_data=df.loc[:,"X1":]
model_data


############################################################
# # 使用主成分分析 手动确定几个主成分 来压缩信息
############################################################

# --- 代码块 6 ---
#查看相关系数 判断使用主成分分析 变量降维的必要性
#你的代码
corr_matrix=model_data.corr()
corr_matrix

# --- 代码块 7 ---
#在使用主成分和聚类之前 应该？？？from sklearn.preprocessing import StandardScaler
#你的代码
from sklearn.preprocessing import StandardScaler
scaler=StandardScaler()
scaler_model_data=scaler.fit_transform(model_data)
scaler_model_data

# --- 代码块 8 ---
#使用sklearn框架做主成分，判断主成分数量
#from sklearn.decomposition import PCA
#你的代码
from sklearn.decomposition import PCA

# --- 代码块 9 ---
#实例化
pca=PCA(n_components=3)
model_data_scale=pca.fit(scaler_model_data)
model_data_scale

# --- 代码块 10 ---
np.set_printoptions(suppress=True)#阻止数字以科学计算输出 眼睛不好观察>0<
#输出主成分方差和占比 pca.explained_variance_
#你的代码
print("主成分可解释的变异：\n",pca.explained_variance_)
print("主成分可解释的变异的比例:\n",pca.explained_variance_ratio_)

# --- 代码块 11 ---
0.8+0.12

# --- 代码块 12 ---
#根据结果 可见 选2个主成分可解释大部分数据


############################################################
# - 根据主成分个数来确定因子个数，为下面因子分析做准备
############################################################


############################################################
# # 因子分析
############################################################

# --- 代码块 15 ---
#导入因子分析的包提取主成分，fa_kit是一个第三方的包 需要下载
#pip install fa_kit 我这里已经下载安装好了。。。

# --- 代码块 16 ---
from fa_kit import FactorAnalysis
from fa_kit import plotting as fa_plotting#绘制因子载荷矩阵

# --- 代码块 17 ---
#对输入的数据进行主成分提取
fa=FactorAnalysis.load_data_samples(
scaler_model_data,
preproc_demean=True,
preproc_scale=True)
fa.extract_components()

# --- 代码块 18 ---
#设定提取主出发的方式，默认是broken_stick，建议使用top_n方法 fa.find
#你的代码
fa.find_comps_to_retain(method="top_n",num_keep=2)

# --- 代码块 19 ---
#通过最大方差法对因子进行旋转
#你的代码
fa.rotate_components(method="varimax")

# --- 代码块 20 ---
#可以绘制因子载荷矩阵图
fa_plotting.graph_summary(fa)
#第一张图解释了数据变异比例，第一个主成分解释了数据80%的变异，前两个主主成分已经大概能够解释原始数据了
#第二张图是在未旋转之前，各变量在因子中权重（载荷）每条折线表示一个因子，x轴个原始变量，y轴不同因子在各个变量上的权重
#第三张图方差最大化旋转后各个因子在各变量上的权重（载荷），观察此图，权重越高，代表性越强
#如果眼睛不喜欢看 emmm 那就看数，即打印因子载荷

# --- 代码块 21 ---
#打印旋转后的因子权重
#你的代码
fa.comps["rot"]


############################################################
# - 输出因子得分 拼接到原数据，对该数据进行层次聚类分析
############################################################

# --- 代码块 23 ---
#输出因子得分，为了方便拼接 转换成数据框
#你的代码n
fa_scores=fa.get_component_scores(scaler_model_data)
fa_scores=pd.DataFrame(fa_scores,columns=["Gross","Avg"])
fa_scores

# --- 代码块 24 ---
#拼接原始数据
#你的代码
cities_fa_scores=df.join(fa_scores)
cities_fa_scores

# --- 代码块 25 ---
cities_fa_scores.to_csv("fa_cities_10.csv",index=False)#不是必须


############################################################
# # 层次聚类分析
############################################################

# --- 代码块 27 ---
#现在，对新的这份数据进行层次聚类分析
#你的代码
new_model_data=pd.read_csv("fa_cities_10.csv")
new_model_data

# --- 代码块 28 ---
#画图，肉眼先看看分成几类，这些城市，
plt.rcParams['font.family'] = 'SimHei'
from pylab import mpl
mpl.rcParams['axes.unicode_minus'] = False 

def scatter(x, y, labels, **kw):
    
    plt.figure(figsize=(6, 4))
    plt.yticks(size=12)
    plt.xticks(size=12)
    plt.scatter(x, y)
    for xx, yy, label in zip(x, y, labels):
        plt.text(xx, yy, '%s.' % label, 
                 ha='center', va='bottom', **kw)
plt.show()

# --- 代码块 29 ---
# 画图，x,y，标签
#你的代码
x=new_model_data["Gross"]
y=new_model_data["Avg"]
labels=new_model_data["AREA"]
scatter(x,y,labels)


############################################################
# - 因子分析后 开始对拼接后的数据进行层次聚类分析
############################################################

# --- 代码块 31 ---
#层次聚类 导入包
import scipy.cluster.hierarchy as sch

# --- 代码块 32 ---
#计算距离 生成点与点欧式距离矩阵
#你的代码
dis_mat=sch.distance.pdist(new_model_data[["Gross","Avg"]],metric='euclidean')

# --- 代码块 33 ---
#搭建层次聚类模型,类与类链接
#你的代码
Z=sch.linkage(dis_mat,method="ward")
Z

# --- 代码块 34 ---
#将层次聚类结果用层次聚类图展示出来，plt.savefig('plot_dendrogram.png')
#你的代码
P=sch.dendrogram(Z,labels=new_model_data["AREA"].tolist())
plt.savefig("plot_dendrogram.png")
