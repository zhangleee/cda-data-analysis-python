# -*- coding: utf-8 -*-
"""
RFM用户价值模型
===============
业务内涵：
    RFM模型是客户价值分析的经典框架，通过三个维度对客户进行分层：
    - R (Recency) 最近一次消费距今天数 → 越小越好，越小说明客户越活跃
    - F (Frequency) 消费频率 → 越大越好，越大说明客户越忠诚
    - M (Monetary) 消费金额 → 越大越好，越大说明客户贡献越高

应用场景：
    1. 会员分层运营：重要价值客户、重要发展客户、重要保持客户、重要挽留客户等
    2. 精准营销：针对不同层级客户推送不同内容
    3. 流失预警：R值突然变大的客户需要及时召回
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# ============================================================
# 1. 模拟销售流水数据（与教材案例对应）
# ============================================================
np.random.seed(42)
n_customers = 500
n_orders = 3000

# 生成客户ID
customer_ids = [f'M{50000 + i}' for i in range(n_customers)]

# 生成订单数据
order_data = []
analysis_date = pd.Timestamp('2021-01-01')  # 分析时点

for _ in range(n_orders):
    cust = np.random.choice(customer_ids)
    # 消费日期分布：大部分在近6个月
    days_ago = np.random.exponential(180)
    order_date = analysis_date - pd.Timedelta(days=days_ago)
    amount = np.random.gamma(shape=2, scale=200)  # 消费金额偏态分布
    order_data.append({
        '客户ID': cust,
        '消费日期': order_date,
        '消费金额': round(amount, 2)
    })

df = pd.DataFrame(order_data)

print("=" * 60)
print(f"原始订单数据: {len(df)} 条记录, {df['客户ID'].nunique()} 个客户")
print("=" * 60)
print(df.head())

# ============================================================
# 2. 计算RFM指标
# ============================================================
# R: 最近一次消费距分析时点的天数
# F: 消费次数
# M: 累计消费金额
rfm = df.groupby('客户ID').agg(
    R=('消费日期', lambda x: (analysis_date - x.max()).days),  # 最近消费距今天数
    F=('消费日期', 'count'),       # 消费次数
    M=('消费金额', 'sum')          # 总消费金额
).reset_index()

print("\n" + "=" * 60)
print("RFM指标汇总")
print("=" * 60)
print(rfm.describe().round(2))

# ============================================================
# 3. RFM打分（5分制）
# ============================================================
# 打分规则：按五分位数打分
# R值越小越好 → 打高分；F和M越大越好 → 打高分

# R打分：最近消费越近分越高
rfm['R_score'] = pd.qcut(rfm['R'], 5, labels=[5, 4, 3, 2, 1]).astype(int)
# F打分：消费次数越多分越高
rfm['F_score'] = pd.qcut(rfm['F'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5]).astype(int)
# M打分：消费金额越高分越高
rfm['M_score'] = pd.qcut(rfm['M'], 5, labels=[1, 2, 3, 4, 5]).astype(int)

# 计算总分
rfm['RFM_total'] = rfm['R_score'] + rfm['F_score'] + rfm['M_score']

print("\n" + "=" * 60)
print("RFM打分明细（前10条）")
print("=" * 60)
print(rfm.head(10).to_string(index=False))

# ============================================================
# 4. 用户分层
# ============================================================
# 以平均值为分界，高于均值为高(↑)，低于均值为低(↓)
R_mean = rfm['R_score'].mean()
F_mean = rfm['F_score'].mean()
M_mean = rfm['M_score'].mean()

def segment_customer(row):
    R_high = row['R_score'] >= R_mean
    F_high = row['F_score'] >= F_mean
    M_high = row['M_score'] >= M_mean

    if R_high and F_high and M_high:
        return '重要价值客户'
    elif R_high and not F_high and M_high:
        return '重要发展客户'
    elif not R_high and F_high and M_high:
        return '重要保持客户'
    elif not R_high and not F_high and M_high:
        return '重要挽留客户'
    elif R_high and F_high and not M_high:
        return '一般价值客户'
    elif R_high and not F_high and not M_high:
        return '一般发展客户'
    elif not R_high and F_high and not M_high:
        return '一般保持客户'
    else:
        return '一般挽留客户'

rfm['客户分层'] = rfm.apply(segment_customer, axis=1)

# 统计各分层客户数
segment_stats = rfm.groupby('客户分层').agg(
    客户数=('客户ID', 'count'),
    平均消费额=('M', 'mean'),
    平均消费频次=('F', 'mean'),
    平均最近消费天数=('R', 'mean')
).round(2).sort_values('客户数', ascending=False)

print("\n" + "=" * 60)
print("客户分层统计")
print("=" * 60)
print(segment_stats.to_string())

# ============================================================
# 5. 可视化
# ============================================================
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 图1：客户分层数量分布
segment_stats['客户数'].plot(kind='barh', ax=axes[0, 0], color='#4c72b0')
axes[0, 0].set_title('各层级客户数量分布', fontweight='bold')
axes[0, 0].set_xlabel('客户数')
axes[0, 0].set_ylabel('')

# 图2：R vs F 散点图
for seg in rfm['客户分层'].unique():
    sub = rfm[rfm['客户分层'] == seg]
    axes[0, 1].scatter(sub['R'], sub['F'], label=seg, alpha=0.6, s=30)
axes[0, 1].set_xlabel('Recency (最近消费天数)')
axes[0, 1].set_ylabel('Frequency (消费频次)')
axes[0, 1].set_title('R-F 客户分布', fontweight='bold')
axes[0, 1].legend(fontsize=8)
axes[0, 1].invert_xaxis()  # R越小越好，反转X轴

# 图3：F vs M 散点图
for seg in rfm['客户分层'].unique():
    sub = rfm[rfm['客户分层'] == seg]
    axes[1, 0].scatter(sub['F'], sub['M'], label=seg, alpha=0.6, s=30)
axes[1, 0].set_xlabel('Frequency (消费频次)')
axes[1, 0].set_ylabel('Monetary (消费金额)')
axes[1, 0].set_title('F-M 客户分布', fontweight='bold')
axes[1, 0].legend(fontsize=8)

# 图4：客户分层消费贡献占比
revenue_by_seg = rfm.groupby('客户分层')['M'].sum()
revenue_by_seg.plot(kind='pie', ax=axes[1, 1], autopct='%1.1f%%', startangle=90)
axes[1, 1].set_title('各层级客户消费贡献占比', fontweight='bold')
axes[1, 1].set_ylabel('')

plt.tight_layout()
plt.savefig('rfm_analysis.png', dpi=150, bbox_inches='tight')
print("\n图表已保存: rfm_analysis.png")

# ============================================================
# 6. 运营建议
# ============================================================
print("\n" + "=" * 60)
print("分层运营策略建议")
print("=" * 60)
strategies = {
    '重要价值客户': 'VIP待遇，专属客服，新品优先体验，维护忠诚度',
    '重要发展客户': '提升消费频次，交叉销售，推荐关联产品',
    '重要保持客户': '唤醒沉睡客户，发送专属优惠券，召回活动',
    '重要挽留客户': '紧急挽回，大力度优惠，调研流失原因',
    '一般价值客户': '常规运营，适度营销，观察成长潜力',
    '一般发展客户': '引导复购，设置消费门槛奖励',
    '一般保持客户': '低成本维护，自动化营销',
    '一般挽留客户': '减少营销投入，自然流失即可'
}
for seg, strategy in strategies.items():
    count = len(rfm[rfm['客户分层'] == seg])
    if count > 0:
        print(f"【{seg}】({count}人) → {strategy}")
