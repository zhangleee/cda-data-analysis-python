# -*- coding: utf-8 -*-
"""
4.1 时间序列预测 - ARIMA基础

知识点说明：
ARIMA模型基础：平稳性检验、ACF/PACF定阶、模型训练与预测。

本文件由CDA教材ipynb转换而来，补充了详细中文注释以帮助理解。
"""

import warnings
warnings.filterwarnings("ignore")


############################################################
# # 1.平稳时间序列分析-ARMA模型
############################################################


############################################################
# 步骤：
# 1.数据预处理 => 2.确定适用模型类型、定阶、差分 => 3.建模 => 4.残差检验（ACF、PACF、DW、正态性检验等等） => 5.预测
############################################################

# --- 代码块 3 ---
import pandas as pd
import numpy as np
from scipy import  stats
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.graphics.api import qqplot
import warnings
import os

%matplotlib inline
warnings.filterwarnings("ignore")

# --- 代码块 4 ---
ts_simu200 = pd.read_csv('ts_simu200.csv',index_col='t')
ts_simu200 .head()


############################################################
# ### 1.1 AR
############################################################


############################################################
# 1.预处理
############################################################

# --- 代码块 7 ---
dates = pd.date_range(start='2017/01/01', periods=200)
ts_simu200.set_index(dates, inplace=True)

dta = ts_simu200['AR1_a']
dta.plot(figsize=(8,5))
plt.show()


############################################################
# 2. 确定模型类型及定阶
############################################################

# --- 代码块 9 ---
# 自相关和偏自相关

sm.graphics.tsa.plot_acf(dta,lags=20)#lags 表示滞后的阶数
sm.graphics.tsa.plot_pacf(dta,lags=20)
plt.show()


############################################################
# 3.建模
############################################################

# --- 代码块 11 ---
ar10 = sm.tsa.ARIMA(dta,order=(1, 0, 0)).fit()


############################################################
# 4.残差检验
# - a. 残差自相关、偏自相关
############################################################

# --- 代码块 13 ---
#检验下残差序列：
resid = ar10.resid

sm.graphics.tsa.plot_acf(resid, lags=20)
sm.graphics.tsa.plot_pacf(resid, lags=20)
plt.show()
# 从残差的ACF和PACF图，可以看到序列残差基本为白噪声


############################################################
# - b. DW检验（一阶自相关)
# DW = 4 <=> ρ= -1　  即存在负自相关性
# DW = 2 <=> ρ= 0　　 即不存在（一阶）自相关性
# DW = 0 <=> ρ= 1     即存在正自相关性。
############################################################

# --- 代码块 15 ---
print(sm.stats.durbin_watson(ar10.resid.values))


############################################################
# - c.残差正态检验
# 观察残差是否符合正态分布,使用正态性检验，也可以使用QQ图进行观察
############################################################

# --- 代码块 17 ---
print(stats.normaltest(resid))

fig, ax = plt.subplots(figsize=(5, 5))
qqplot(resid, line='q', fit=True, ax=ax)
plt.show()


############################################################
# 5. 预测
############################################################

# --- 代码块 19 ---
# 预测: ar.predict 或者 ar.forcast
forcast= ar10.forecast(steps=5) 
print(pd.DataFrame({'forcast': forcast}))


############################################################
# ### 1.2 MA
############################################################


############################################################
# 1. 预处理（略）
# 2. 模型选择、定阶
############################################################

# --- 代码块 22 ---
dta = ts_simu200['MA1_a']

# 自相关和偏自相关
sm.graphics.tsa.plot_acf(dta,lags=20) #  lags 表示滞后的阶数
sm.graphics.tsa.plot_pacf(dta,lags=20)
plt.show()


############################################################
# 3. 建模
############################################################

# --- 代码块 24 ---
#  拟合数据
ma01 = sm.tsa.ARIMA(dta,order=(0, 0, 1)).fit()


############################################################
# 4. 残差检验
############################################################

# --- 代码块 26 ---
resid = ma01.resid

#  通过自相关检验残差
sm.graphics.tsa.plot_acf(resid.values.squeeze(), lags=20)
sm.graphics.tsa.plot_pacf(resid, lags=20)
plt.show()

# --- 代码块 27 ---
print(sm.stats.durbin_watson(ma01.resid))
print(stats.normaltest(resid).pvalue)


############################################################
# 5. 预测
############################################################

# --- 代码块 29 ---
ma01.predict(start=pd.to_datetime('2017-07-20'),
             end=pd.to_datetime('2017-07-25'),
             dynamic=False)


############################################################
# ### 1.3 ARMA
############################################################


############################################################
# 1. 预处理（略）
# 2. 模型选择、定阶
############################################################

# --- 代码块 32 ---
dta=ts_simu200['ARMA_11_b']

sm.graphics.tsa.plot_acf(dta,lags=20)#lags 表示滞后的阶数
sm.graphics.tsa.plot_pacf(dta,lags=20)
plt.show()

# --- 代码块 33 ---
# 暴力搜索最佳的自回归与移动平均的阶数

import warnings
import itertools

warnings.filterwarnings("ignore")  # 忽略ARIMA模型无法估计出结果时的报警信息

# 设置自相关(AR)、差分(I)、移动平均(MA)的三个参数的取值范围
p = d = q = range(0, 2)
pdq = list(itertools.product(p, d, q))

best_aic = np.inf
best_pdq = None
best_seasonal_pdq = None
temp_model = None

for param in pdq:
    try:
        temp_model = sm.tsa.ARIMA(dta,param)
        results = temp_model.fit()
        if results.aic < best_aic:
            best_aic = results.aic
            best_pdq = param
            best_seasonal_pdq = param_seasonal
    except:
        continue
        
print("Best ARIMA{} model - AIC:{}".format(best_pdq, best_aic))


############################################################
# 3. 建模
############################################################

# --- 代码块 35 ---
arma11 = sm.tsa.ARIMA(dta,order=(1, 0, 1)).fit()


############################################################
# 4. 残差检验
############################################################

# --- 代码块 37 ---
resid = arma11.resid

sm.graphics.tsa.plot_acf(resid.values.squeeze(), lags=20)
sm.graphics.tsa.plot_pacf(resid, lags=20)
plt.show()

# --- 代码块 38 ---
print(sm.stats.durbin_watson(arma11.resid))
print(stats.normaltest(resid).pvalue)


############################################################
# 5. 预测
############################################################

# --- 代码块 40 ---
arma11.predict(start=200,
               end=205,
               dynamic=False)


############################################################
# # 2.非平稳时间序列分析-ARIMA模型
############################################################


############################################################
# 1. 预处理（略）
# 2. 平稳性检验、差分、定阶
############################################################

# --- 代码块 43 ---
from statsmodels.tsa.stattools import adfuller

dta = ts_simu200['ARIMA_110']

#平稳性检验
result = adfuller(dta)
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])

# --- 代码块 44 ---
#原序列的自相关和偏自相关
sm.graphics.tsa.plot_acf(dta,lags=20)
sm.graphics.tsa.plot_pacf(dta,lags=20)
plt.show()

# --- 代码块 45 ---
dta.plot()

# --- 代码块 46 ---
diff1= dta.diff(1)
diff1.plot(figsize=(8, 5))
plt.show()

# --- 代码块 47 ---
print('p-value: %f' % adfuller(diff1[1:])[1])

# --- 代码块 48 ---
p = d = q = range(0, 2)
pdq = list(itertools.product(p, d, q))

best_aic = np.inf
best_pdq = None
best_seasonal_pdq = None
temp_model = None

for param in pdq:
    try:
        temp_model = sm.tsa.ARIMA(dta,param)
        results = temp_model.fit()
        if results.aic < best_aic:
            best_aic = results.aic
            best_pdq = param
    except:
        continue
        
print("Best ARIMA{} model - AIC:{}".format(best_pdq, best_aic))


############################################################
# 3. 建模
############################################################

# --- 代码块 50 ---
arima110 = sm.tsa.ARIMA(dta,order=(1, 1, 0)).fit()


############################################################
# 4. 残差检验（略）
# 5. 预测（略）
############################################################
