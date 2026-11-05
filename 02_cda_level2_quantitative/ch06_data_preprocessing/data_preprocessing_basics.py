# -*- coding: utf-8 -*-
"""
第6章 数据预处理 - 预处理基础

知识点说明：
本章讲解数据预处理全流程：缺失值填充、异常值检测、类别变量编码、WOE编码、变量标准化/归一化等，为建模做准备。

本文件由CDA教材ipynb转换而来，补充了详细中文注释以帮助理解。
"""

import warnings
warnings.filterwarnings("ignore")

# --- 代码块 1 ---
import pandas as pd
import os
import numpy as np
# 导入数据
camp = pd.read_csv(r"teleco_camp_orig.csv")
# 脏数据或数据不正确
import matplotlib.pyplot as plt
plt.hist(camp["AvgIncome"],bins=20)#,normed=True)#查看分布情况

# --- 代码块 2 ---
camp["AvgIncome"].describe(include="all")

# --- 代码块 3 ---
camp["AvgHomeValue"].describe(include="all")

# --- 代码块 4 ---
#这里的 0值应该是缺失值，处理 0值。
camp["AvgIncome"]=camp["AvgIncome"].replace({0:np.NaN})

# --- 代码块 5 ---
#像这种外部获取的数据要比较小心，经常出现意义不清晰或这错误值。AvgHomeValue也有这种情况
plt.hist(camp["AvgIncome"],bins=20,range=(camp.AvgIncome.min(),camp.AvgIncome.max()))
#由于数据中存在缺失值 ,需要指定绘图的值域

# --- 代码块 6 ---
camp["AvgHomeValue"].describe(include="all")
