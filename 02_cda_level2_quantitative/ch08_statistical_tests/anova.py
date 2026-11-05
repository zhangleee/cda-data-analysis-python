# -*- coding: utf-8 -*-
"""
第8章 统计检验 - 方差分析(ANOVA)

知识点说明：
方差分析用于检验三个及以上总体均值是否存在显著差异，包括单因素方差分析和多因素方差分析。

本文件由CDA教材ipynb转换而来，补充了详细中文注释以帮助理解。
"""

import warnings
warnings.filterwarnings("ignore")


############################################################
# # 单因素方差分析
############################################################

# --- 代码块 2 ---
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
import pandas as pd

# --- 代码块 3 ---
data = pd.read_csv('creditcard_exp.csv')
df = data[['avg_exp','edu_class','gender']].dropna(how='any',axis=0)
df['edu_class'] = df['edu_class'].astype('str')
df['gender'] = df['gender'].astype('str')

# --- 代码块 4 ---
df['avg_exp'] = df['avg_exp'].apply(lambda x: 0 if x==' ' else x)
df['avg_exp'] = df['avg_exp'].astype('float')

# --- 代码块 5 ---
formula = f'avg_exp ~ C(edu_class) + C(gender)'
anova = ols(formula=formula, data=df).fit()
anova_results = anova.summary()
print(anova_results)


############################################################
# # 多因素方差分析
############################################################

# --- 代码块 7 ---
data = pd.read_csv('creditcard_exp.csv')
df = data[['avg_exp','edu_class','gender']].dropna(how='any',axis=0)
df['edu_class'] = df['edu_class'].astype('str')
df['gender'] = df['gender'].astype('str')
df['avg_exp'] = df['avg_exp'].apply(lambda x: 0 if x==' ' else x)
df['avg_exp'] = df['avg_exp'].astype('float')

# --- 代码块 8 ---
formula = f'avg_exp ~ C(edu_class) + C(gender) + C(edu_class)*C(gender)'

anova = ols(formula=formula, data=df).fit()
anova_results = anova.summary()
print(anova_results)
