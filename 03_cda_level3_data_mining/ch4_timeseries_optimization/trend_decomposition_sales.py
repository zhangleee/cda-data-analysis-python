# -*- coding: utf-8 -*-
"""
4.1.1 时间序列预测 - 趋势分解法

知识点说明：
时间序列经典分解方法（趋势+季节+残差），用于理解时间序列的构成要素。

本文件由CDA教材ipynb转换而来，补充了详细中文注释以帮助理解。
"""

import warnings
warnings.filterwarnings("ignore")


############################################################
# ##### 先安装：http://landinghub.visualstudio.com/visual-cpp-build-tools
# - ```pip install pystan```
# - ```pip install fbprophet```  or  ```conda install -c conda-forge fbprophet```
# - ```conda install plotly -y ```
############################################################

# --- 代码块 2 ---
%matplotlib inline
import pandas as pd
from fbprophet import Prophet
import matplotlib.pyplot as plt
import os
import warnings

warnings.filterwarnings("ignore")


############################################################
# ### 1、导入数据，预处理
############################################################

# --- 代码块 4 ---
df = pd.read_csv('air.csv')
df['DATE'] = pd.to_datetime(df['DATE'])
df.head()

# --- 代码块 5 ---
df.dtypes

# --- 代码块 6 ---
df['DATE'] = pd.DatetimeIndex(df['DATE'])
df.dtypes

# --- 代码块 7 ---
# 按照fbprophet的输入限制，传入的DataFrame.columns 必须为['ds', 'y']
df = df.rename(columns={'DATE': 'ds', 'AIR': 'y'})
df.head(2)

# --- 代码块 8 ---
ax = df.set_index('ds').plot(figsize=(8, 5))
ax.set_title('Monthly Number of Airline Passengers', fontsize=15)
ax.set_xlabel('Date', fontsize=15)
plt.show()


############################################################
# ### 使用加法模型
############################################################

# --- 代码块 10 ---
# 设置趋势的形式和预测值的置信区间为95% 
my_model = Prophet(
    growth='linear',
    yearly_seasonality='auto',
    weekly_seasonality=False, 
    seasonality_mode='additive',
    daily_seasonality=False,
    holidays=None,
    interval_width=0.95, 
)
my_model.fit(df)


############################################################
# 预测
############################################################

# --- 代码块 12 ---
future_dates = my_model.make_future_dataframe(periods=36, freq='MS')
forecast = my_model.predict(future_dates)

forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(5)

# --- 代码块 13 ---
fig, ax = plt.subplots(figsize=(8, 5))
ax.set_title('Forcast of Airline Passengers', fontsize=15)
my_model.plot(forecast, ax=ax, uncertainty=True)
plt.show()


############################################################
# 图形上看，残差异方差比较明显！因此：
# ### 使用乘法模型
############################################################

# --- 代码块 15 ---
# 带节日效应的乘法模型建模
my_model = Prophet(
    growth='linear', 
    seasonality_mode='multiplicative',
    holidays=None,
    interval_width=0.95
)

# 增加节假日效应
my_model.add_country_holidays('China')

my_model.fit(df)


############################################################
# 节假日可以自定义，lower_window和upper_window代表节日向下(向上)影响的天数，此处仅做示例：
#
# ```
# programmers_day = pd.DataFrame({
# 'holiday': 'Chrismas',
# 'ds': pd.to_datetime(['1957-10-24', '1958-10-24', '1959-10-24']),
# 'lower_window': 3,
# 'upper_window': 0,
# })
#
# shopping_day = pd.DataFrame({
# 'holiday': 'New_year',
# 'ds': pd.to_datetime(['1957-11-11', '1958-11-11', '1959-11-11']),
# 'lower_window': 1,
# 'upper_window': 0,
# })
#
# holidays = pd.concat((programmers_day, shopping_day))
#
# my_model = Prophet(
# growth='linear',
# seasonality_mode='multiplicative',
# holidays=holidays,
# interval_width=0.95
# )
# ```
############################################################

# --- 代码块 17 ---
from fbprophet.plot import add_changepoints_to_plot

#  预测
future_dates = my_model.make_future_dataframe(periods=36, freq='MS')
forecast = my_model.predict(future_dates)

#  绘图
fig, ax = plt.subplots(figsize=(8, 5))
ax.set_title('Forcast of Airline Passengers', fontsize=15)
my_model.plot(forecast,uncertainty=True, ax=ax)   

#  绘制changepoints
add_changepoints_to_plot(ax, my_model, forecast)  
plt.show()

# --- 代码块 18 ---
my_model.plot_components(forecast, figsize=(7, 5))
plt.show()

# --- 代码块 19 ---
forecast.tail(5)
