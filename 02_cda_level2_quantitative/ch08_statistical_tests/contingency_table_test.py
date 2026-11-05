# -*- coding: utf-8 -*-
"""
第8章 统计检验 - 列联表卡方检验

知识点说明：
卡方检验用于检验两个分类变量是否独立，通过列联表分析变量间的关联关系。

本文件由CDA教材ipynb转换而来，补充了详细中文注释以帮助理解。
"""

import warnings
warnings.filterwarnings("ignore")

# --- 代码块 1 ---
import pandas as pd
accepts =pd.read_csv ( 'accepts.csv' )
cross_table=pd.crosstab(accepts.bankruptcy_ind,accepts.bad_ind, margins=True)
cross_table

# --- 代码块 2 ---
cross_table_rowpct = cross_table.div(cross_table ["All"] ,axis = 0)
cross_table_rowpct

# --- 代码块 3 ---
# 打印结果
from scipy import stats
print(
    "chisq = %6.4f\np-value = %6.4f\ndof = %d\nexpected_freq = %s"
    %stats.chi2_contingency (cross_table))
