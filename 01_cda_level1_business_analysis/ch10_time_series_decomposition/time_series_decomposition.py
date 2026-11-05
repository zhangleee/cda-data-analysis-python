# -*- coding: utf-8 -*-
"""
效应分解法做时间序列预报
========================
业务内涵：
    时间序列分解（效应分解）将历史数据拆解为四个组成部分：
    - 趋势项(T)：长期上升或下降的方向
    - 季节项(S)：固定周期的波动（月度/季度/节假日）
    - 循环项(C)：经济周期等中长期波动
    - 残差项(I)：随机噪声

    分解后可以分别预测各部分，再组合得到最终预测。
    这是Excel/WPS做时间序列预测的核心方法。

教材案例：信用卡消费额预测、航空乘客数预测(AirPassengers)
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# ============================================================
# 1. 加载数据：航空乘客数（经典时间序列数据集）
# ============================================================
# AirPassengers: 1949-1960年每月国际航空乘客数（千人）
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/airline-passengers.csv"
try:
    df = pd.read_csv(url, parse_dates=['Month'], index_col='Month')
    df.columns = ['乘客数']
except:
    # 离线备用：生成模拟数据
    dates = pd.date_range('1949-01-01', '1960-12-31', freq='MS')
    trend = np.linspace(100, 500, len(dates))
    season = 50 * np.sin(2 * np.pi * np.arange(len(dates)) / 12)
    noise = np.random.normal(0, 10, len(dates))
    df = pd.DataFrame({'乘客数': trend + season + noise}, index=dates)

print("=" * 60)
print("航空乘客数时间序列数据")
print("=" * 60)
print(df.head())
print(f"\n时间范围: {df.index[0].strftime('%Y-%m')} ~ {df.index[-1].strftime('%Y-%m')}")
print(f"数据点: {len(df)} 个月")

# ============================================================
# 2. 效应分解（加法模型 vs 乘法模型）
# ============================================================
# 加法模型: y = T + S + I
# 乘法模型: y = T × S × I （适合波动随趋势增大的序列）

# 乘法分解（航空数据通常用乘法，因为波动幅度随趋势增大）
decomposition = seasonal_decompose(df['乘客数'], model='multiplicative', period=12)

fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)

axes[0].plot(df.index, df['乘客数'], label='原始数据', color='black')
axes[0].set_ylabel('原始值')
axes[0].set_title('时间序列效应分解（乘法模型）', fontsize=14, fontweight='bold')
axes[0].legend()

axes[1].plot(decomposition.trend.index, decomposition.trend, label='趋势项(T)', color='blue')
axes[1].set_ylabel('趋势')
axes[1].legend()

axes[2].plot(decomposition.seasonal.index, decomposition.seasonal, label='季节项(S)', color='green')
axes[2].set_ylabel('季节因子')
axes[2].legend()

axes[3].plot(decomposition.resid.index, decomposition.resid, label='残差项(I)', color='red')
axes[3].set_ylabel('残差')
axes[3].legend()

plt.tight_layout()
plt.savefig('time_series_decomposition.png', dpi=150, bbox_inches='tight')
print("\n分解图已保存: time_series_decomposition.png")
plt.show()

# ============================================================
# 3. 使用Holt-Winters指数平滑法预测
# ============================================================
# Holt-Winters 是效应分解思想的经典实现：
# - 水平项(level) + 趋势项(trend) + 季节项(seasonal)
# 适合有明显趋势和季节性的时间序列预测

# 训练集：前10年，测试集：后2年
train = df[:'1959-12-01']
test = df['1960-01-01':]

# 拟合Holt-Winters模型
model = ExponentialSmoothing(train['乘客数'],
                              trend='mul',      # 乘法趋势
                              seasonal='mul',   # 乘法季节
                              seasonal_periods=12).fit()

# 预测
forecast = model.forecast(len(test))

print("\n" + "=" * 60)
print("预测效果对比（1960年）")
print("=" * 60)
compare = pd.DataFrame({
    '实际值': test['乘客数'],
    '预测值': forecast.round(1),
    '误差%': ((test['乘客数'] - forecast) / test['乘客数'] * 100).round(2)
})
print(compare.to_string())

# 计算MAPE
mape = np.mean(np.abs((test['乘客数'] - forecast) / test['乘客数'])) * 100
print(f"\n测试集MAPE（平均绝对百分比误差）: {mape:.2f}%")

# ============================================================
# 4. 未来24个月预测
# ============================================================
future_forecast = model.forecast(24)

# 绘图
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df.index, df['乘客数'], label='历史数据', color='black')
future_idx = pd.date_range(df.index[-1], periods=25, freq='MS')[1:]
ax.plot(future_idx, future_forecast, label='未来24个月预测',
        color='red', linestyle='--', linewidth=2)
ax.axvline(df.index[-1], color='gray', linestyle=':', alpha=0.5)
ax.set_title('航空乘客数预测（Holt-Winters效应分解法）', fontsize=14, fontweight='bold')
ax.set_xlabel('年份')
ax.set_ylabel('乘客数（千人）')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('time_series_forecast.png', dpi=150, bbox_inches='tight')
print("预测图已保存: time_series_forecast.png")
plt.show()

# ============================================================
# 5. 方法总结
# ============================================================
print("\n" + "=" * 60)
print("效应分解法要点")
print("=" * 60)
print("""
1. 适用场景：
   - 数据有明显趋势和季节性
   - 短期预测（1-2个周期内）
   - 业务人员需要直观理解数据构成

2. 加法 vs 乘法模型选择：
   - 加法：季节波动幅度不随趋势变化 → 用加法
   - 乘法：波动幅度随趋势增大（如业务增长后波动也变大）→ 用乘法

3. 优点：
   - 直观易懂，业务可解释性强
   - 能分离出趋势和季节因素，便于归因分析
   - Excel/WPS内置功能即可实现

4. 局限：
   - 不能捕捉突变和拐点
   - 长期预测误差会累积
   - 适合稳定业务，不适合剧烈变化场景
""")
