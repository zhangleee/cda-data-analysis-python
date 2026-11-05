# -*- coding: utf-8 -*-
"""
六类基础分析方法
================
CDA教材核心：趋势分析、对比分析、构成分析、分布分析、关系分析、桑基图
这六种是商业数据分析最基础也最常用的分析视角。
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# ============================================================
# 模拟销售数据
# ============================================================
np.random.seed(42)
dates = pd.date_range('2023-01-01', '2023-12-31', freq='D')
regions = ['华东', '华北', '华南', '西南', '华中']
products = ['手机', '电脑', '耳机', '手表', '平板']

data = []
for date in dates:
    for region in regions:
        for product in products:
            amount = np.random.exponential(5000)
            data.append({
                '日期': date,
                '地区': region,
                '产品': product,
                '销售额': amount
            })

df = pd.DataFrame(data)
df['月份'] = df['日期'].dt.month

print("=" * 60)
print(f"模拟数据: {len(df)} 条销售记录")
print("=" * 60)

# ============================================================
# 1. 趋势分析：随时间变化的走向
# ============================================================
print("\n" + "=" * 60)
print("1. 趋势分析：月度销售额走势")
print("=" * 60)

monthly_sales = df.groupby('月份')['销售额'].sum()

fig, ax = plt.subplots(figsize=(10, 5))
monthly_sales.plot(kind='line', marker='o', ax=ax, color='#2196F3', linewidth=2)
ax.set_title('月度销售额趋势', fontweight='bold')
ax.set_xlabel('月份')
ax.set_ylabel('销售额（元）')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('01_trend_analysis.png', dpi=150)
print("图表已保存: 01_trend_analysis.png")

# ============================================================
# 2. 对比分析：不同维度横向比较
# ============================================================
print("\n" + "=" * 60)
print("2. 对比分析：各地区销售额对比")
print("=" * 60)

region_sales = df.groupby('地区')['销售额'].sum().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(10, 5))
region_sales.plot(kind='bar', ax=ax, color='#4CAF50')
ax.set_title('各地区销售额对比', fontweight='bold')
ax.set_xlabel('地区')
ax.set_ylabel('销售额（元）')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('02_comparison_analysis.png', dpi=150)
print("图表已保存: 02_comparison_analysis.png")

# ============================================================
# 3. 构成分析：部分占整体的比例
# ============================================================
print("\n" + "=" * 60)
print("3. 构成分析：各产品销售额占比")
print("=" * 60)

product_sales = df.groupby('产品')['销售额'].sum()

fig, ax = plt.subplots(figsize=(8, 8))
product_sales.plot(kind='pie', ax=ax, autopct='%1.1f%%', startangle=90)
ax.set_title('产品销售额构成', fontweight='bold')
ax.set_ylabel('')
plt.tight_layout()
plt.savefig('03_composition_analysis.png', dpi=150)
print("图表已保存: 03_composition_analysis.png")

# ============================================================
# 4. 分布分析：数据的分布形态
# ============================================================
print("\n" + "=" * 60)
print("4. 分布分析：单日销售额分布")
print("=" * 60)

daily_sales = df.groupby('日期')['销售额'].sum()

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
daily_sales.plot(kind='hist', bins=30, ax=axes[0], color='#FF9800', edgecolor='white')
axes[0].set_title('单日销售额分布（直方图）', fontweight='bold')
axes[0].set_xlabel('日销售额')

daily_sales.plot(kind='box', ax=axes[1], color='#FF9800')
axes[1].set_title('单日销售额分布（箱线图）', fontweight='bold')
axes[1].set_ylabel('日销售额')

plt.tight_layout()
plt.savefig('04_distribution_analysis.png', dpi=150)
print("图表已保存: 04_distribution_analysis.png")

# ============================================================
# 5. 关系分析：两个变量之间的关系
# ============================================================
print("\n" + "=" * 60)
print("5. 关系分析：温度与销售额的关系（示例）")
print("=" * 60)

# 模拟温度数据
np.random.seed(42)
temperature = np.random.uniform(0, 35, len(daily_sales))
sales_corr = daily_sales.values + (temperature - 15) * 1000  # 温度越高销售越高

fig, ax = plt.subplots(figsize=(10, 5))
ax.scatter(temperature, sales_corr, alpha=0.6)
z = np.polyfit(temperature, sales_corr, 1)
p = np.poly1d(z)
ax.plot(temperature, p(temperature), "r--", linewidth=2)
ax.set_title('温度与销售额关系', fontweight='bold')
ax.set_xlabel('温度（℃）')
ax.set_ylabel('日销售额（元）')
plt.tight_layout()
plt.savefig('05_relation_analysis.png', dpi=150)
print("图表已保存: 05_relation_analysis.png")

# ============================================================
# 6. 桑基图（Sankey Diagram）：流量流转分析
# ============================================================
print("\n" + "=" * 60)
print("6. 桑基图：用户路径流转分析")
print("=" * 60)

# 模拟用户转化路径数据
# 网站 → 浏览商品 → 加购 → 下单 → 支付
sankey_data = pd.DataFrame({
    '阶段': ['首页浏览', '搜索商品', '查看详情', '加入购物车', '提交订单', '完成支付'],
    '用户数': [10000, 7000, 4500, 2800, 1500, 900]
})

print(sankey_data.to_string(index=False))
print("\n注：桑基图在PowerBI中通过自定义视觉对象实现，")
print("    Python可用plotly.graph_objects.Sankey绘制")

# ============================================================
# 方法总结
# ============================================================
print("\n" + "=" * 60)
print("六类分析方法总结")
print("=" * 60)
print("""
| 分析方法 | 回答什么问题 | 常用图表 |
|---------|-------------|---------|
| 趋势分析 | 随时间怎么变？ | 折线图 |
| 对比分析 | 谁高谁低？ | 柱状图/条形图 |
| 构成分析 | 占比多少？ | 饼图/堆叠柱状图 |
| 分布分析 | 数据长什么样？ | 直方图/箱线图 |
| 关系分析 | 两个变量有关吗？ | 散点图/相关系数 |
| 桑基图分析 | 流量怎么流转？ | 桑基图 |

这六种是数据分析的「基本动作」，复杂分析都是它们的组合。
""")
