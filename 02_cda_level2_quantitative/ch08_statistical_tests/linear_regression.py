# -*- coding: utf-8 -*-
"""
第8章 统计检验 - 线性回归

知识点说明：
线性回归是最基础的预测模型，通过最小二乘法拟合因变量与自变量的线性关系，用于预测和解释。

本文件由CDA教材ipynb转换而来，补充了详细中文注释以帮助理解。
"""

import warnings
warnings.filterwarnings("ignore")

# --- 代码块 1 ---
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"


############################################################
# ## 读取变量
############################################################

# --- 代码块 3 ---
import numpy as np
import pandas as pd

# --- 代码块 4 ---
#读取数据
data_raw = pd.read_excel('LR_practice.xlsx')
data_raw.head()

# --- 代码块 5 ---
data_raw.tail()

# --- 代码块 6 ---
data_raw.head(2)

# --- 代码块 7 ---
#数据基本信息
data_raw.info()


############################################################
# ## 数据清洗
############################################################


############################################################
# ### 删除无用变量
############################################################

# --- 代码块 10 ---
#变量'id','Acc','edad2'
data_raw.drop(['id','Acc','edad2'], axis=1, inplace=True)

# --- 代码块 11 ---
data_raw.head(2)


############################################################
# ### 重复值
############################################################

# --- 代码块 13 ---
#删除重复值
data_raw.drop_duplicates(inplace=True)


############################################################
# ### 缺失值
############################################################

# --- 代码块 15 ---
#查看缺失情况
data_raw.isnull().mean()

# --- 代码块 16 ---
data_raw.isnull().sum()


############################################################
# #### 填补缺失值
############################################################

# --- 代码块 18 ---
data_raw['avg_exp'].mean()

# --- 代码块 19 ---
#avg_exp
data_raw['avg_exp'] = data_raw['avg_exp'].fillna(data_raw['avg_exp'].mean())

# --- 代码块 20 ---
data_raw.isnull().mean()


############################################################
# #### 数据编码和缺失值
############################################################

# --- 代码块 22 ---
#方法1：gender
data_raw['gender'] = data_raw['gender'].map({'Male':1, 'Female':0})

# --- 代码块 23 ---
data_raw.head(2)

# --- 代码块 24 ---
#方法2：edu_class
data_raw['edu_class'].unique()

# --- 代码块 25 ---
label = data_raw['edu_class'].unique().tolist()
label

# --- 代码块 26 ---
label.index('中学')

# --- 代码块 27 ---
#对原数据进行编码
data_raw['edu_class'] = data_raw['edu_class'].apply(lambda x: label.index(x))

# --- 代码块 28 ---
data_raw.head()

# --- 代码块 29 ---
data_raw['edu_class'].value_counts()


############################################################
# ### 异常值
############################################################


############################################################
# #### 箱线图
############################################################

# --- 代码块 32 ---
import seaborn as sns

# --- 代码块 33 ---
# dist_avg_income
sns.boxplot(data=data_raw['dist_avg_income'])


############################################################
# #### 3倍标准差
############################################################

# --- 代码块 35 ---
from scipy import stats

# --- 代码块 36 ---
#标准化数据(Age)
z = stats.zscore(data_raw['Age'])
z

# --- 代码块 37 ---
(z>3)|(z<-3)

# --- 代码块 38 ---
#寻找异常数据的索引
z[(z>3)|(z<-3)]

# --- 代码块 39 ---
#查看异常数据的值
data_raw['Age'].iloc[40]


############################################################
# 如何填补999这个异常的年龄数据呢？
############################################################

# --- 代码块 41 ---
data_raw['Age'].mean()

# --- 代码块 42 ---
data_raw['Age'].drop(index=40).mean()

# --- 代码块 43 ---
#将异常值使用除异常值之外的数据的均值进行填补
data_raw['Age'].iloc[40] = data_raw['Age'].drop(index=40).mean()


############################################################
# ### 哑变量转换
############################################################

# --- 代码块 45 ---
data_raw.head()

# --- 代码块 46 ---
#edu_class
dummy = pd.get_dummies(data=data_raw['edu_class'], prefix='edu', drop_first=True)
dummy

# --- 代码块 47 ---
#合并到原数据
data = pd.concat([data_raw, dummy], axis=1)
data.head()


############################################################
# ## 相关分析
############################################################


############################################################
# ### 相关系数
############################################################

# --- 代码块 50 ---
data.corr()

# --- 代码块 51 ---
#分类变量
data.corr(method='kendall')


############################################################
# ### 散点图
############################################################

# --- 代码块 53 ---
import matplotlib.pyplot as plt

# --- 代码块 54 ---
# avg_exp和Income
plt.scatter(data['Income'], data['avg_exp'])


############################################################
# ## 回归分析
############################################################


############################################################
# ### 回归模型
############################################################

# --- 代码块 57 ---
from statsmodels.formula.api import ols

# --- 代码块 58 ---
data.columns

# --- 代码块 59 ---
data.head()

# --- 代码块 60 ---
# model_1 = ols(LR1, data)
# model_1 = model_1.fit()

# --- 代码块 61 ---
LR1 = 'avg_exp~gender+Age+ Income+ Ownrent+ Selfempl+dist_home_val+ dist_avg_income+edu_1+ edu_2+edu_3+ edu_4'
model_1 = ols(LR1, data).fit()

# --- 代码块 62 ---
model_1.summary()

# --- 代码块 63 ---
#常用接口
dir(model_1)

# --- 代码块 64 ---
model_1.resid


############################################################
# ### 模型调优
############################################################


############################################################
# #### 共线性
############################################################

# --- 代码块 67 ---
data.head()

# --- 代码块 68 ---
def vif(df, y_col):
    x_cols = list(df.columns)
    x_cols.remove(y_col)
    formula = y_col + '~' + '+'.join(x_cols)
    rsquared = ols(formula, df).fit().rsquared
    return 1. / (1. - rsquared)

exog = data[['gender','Age','Income','Ownrent','Selfempl','dist_home_val','dist_avg_income','edu_class']]

for y_col in exog.columns:
    print(y_col, '\t', vif(df=exog, y_col=y_col))

# --- 代码块 69 ---
#重新拟合模型
LR2 = 'avg_exp~gender+Age+ Income+ Ownrent+ Selfempl+dist_home_val+edu_1+ edu_2+edu_3+ edu_4'
model_2 = ols(LR2, data).fit()
model_2.summary()


############################################################
# #### 同方差
############################################################


############################################################
# 残差图：
# - 一元回归：横坐标是X，纵坐标是残差
# - 多元回归：横坐标是Y的拟合值，纵坐标是残差
############################################################

# --- 代码块 72 ---
#残差图
plt.scatter(model_2.predict(data), model_2.resid)


############################################################
# #### 正态性
############################################################

# --- 代码块 74 ---
res = stats.probplot(model_2.resid, plot=plt)

# --- 代码块 75 ---
data['ln_avg_exp'] = np.log(data['avg_exp'])
data.head()

# --- 代码块 76 ---
#重新拟合模型
LR3 = 'ln_avg_exp~gender+Age+ Income+ Ownrent+ Selfempl+dist_home_val+edu_1+ edu_2+edu_3+ edu_4'
model_3 = ols(LR3, data).fit()
model_3.summary()


############################################################
# ![image.png](attachment:image.png)
############################################################

# --- 代码块 78 ---
res = stats.probplot(model_3.resid, plot=plt)


############################################################
# #### 高次项
############################################################

# --- 代码块 80 ---
data['Age_sq'] = data['Age']**2
data.head()

# --- 代码块 81 ---
#年龄
LR4 = 'ln_avg_exp~gender+Age+ Income+ Ownrent+ Selfempl+dist_home_val+edu_1+ edu_2+edu_3+ edu_4 + Age_sq'
model_4 = ols(LR4, data).fit()
model_4.summary()


############################################################
# #### 交互项
############################################################

# --- 代码块 83 ---
data['Age_gender'] = data['Age']*data['gender']
data.head()

# --- 代码块 84 ---
LR5 = 'ln_avg_exp~gender+Age+ Income+ Ownrent+ Selfempl+dist_home_val+edu_1+ edu_2+edu_3+ edu_4 + Age_sq+Age_gender'
model_5 = ols(LR5, data).fit()
model_5.summary()
