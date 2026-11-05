# -*- coding: utf-8 -*-
"""
同期群分析（Cohort Analysis）
=============================
业务内涵：
    同期群分析将用户按「首次行为时间」分组，追踪每组用户在后续时间的留存/活跃情况。
    常用于：
    - 用户留存分析：新注册用户在第1天、第7天、第30天的留存率
    - 复购分析：不同月份首购客户的复购率变化
    - 产品迭代效果验证：新版本上线后，新用户留存是否提升

核心价值：
    避免用整体平均值掩盖问题，能看出不同时期获取的用户质量差异。
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# ============================================================
# 1. 模拟用户登录数据（与教材案例对应）
# ============================================================
np.random.seed(42)
n_users = 2000

# 注册日期：2020年7月-12月，按月分组
reg_dates = pd.date_range('2020-07-01', '2020-12-31', freq='D')
users = pd.DataFrame({
    '用户ID': [f'U{10000+i}' for i in range(n_users)],
    '注册日期': np.random.choice(reg_dates, n_users)
})

# 生成登录记录：每个用户注册后有一定概率在后续天数登录
login_records = []
for _, user in users.iterrows():
    reg = user['注册日期']
    # 留存率随天数衰减
    max_days = np.random.randint(7, 180)
    for day in range(max_days):
        # 留存概率：第1天高，之后指数衰减
        retain_prob = 0.6 * np.exp(-day / 30)
        if np.random.random() < retain_prob:
            login_date = reg + pd.Timedelta(days=day)
            login_records.append({
                '用户ID': user['用户ID'],
                '登录日期': login_date
            })

logins = pd.DataFrame(login_records)
print("=" * 60)
print(f"用户数: {len(users)}, 登录记录数: {len(logins)}")
print("=" * 60)

# ============================================================
# 2. 构建同期群（按月分组）
# ============================================================
# 注册月份作为同期群
users['注册月份'] = users['注册日期'].dt.to_period('M')
logins['登录月份'] = logins['登录日期'].dt.to_period('M')

# 合并
user_logins = logins.merge(users[['用户ID', '注册月份']], on='用户ID')

# 计算每个用户在注册后第几个月活跃
user_logins['注册后第N月'] = (
    user_logins['登录月份'].dt.year - user_logins['注册月份'].dt.year
) * 12 + (
    user_logins['登录月份'].dt.month - user_logins['注册月份'].dt.month
)

# ============================================================
# 3. 计算留存矩阵
# ============================================================
# 每个同期群的初始用户数
cohort_size = users.groupby('注册月份')['用户ID'].nunique()

# 每个同期群在第N月的活跃用户数
cohort_retention = user_logins.groupby(['注册月份', '注册后第N月'])['用户ID'].nunique().unstack()

# 计算留存率
retention_rate = cohort_retention.divide(cohort_size, axis=0)

print("\n" + "=" * 60)
print("同期群留存率矩阵")
print("=" * 60)
print(retention_rate.round(3))

# ============================================================
# 4. 绘制留存热力图
# ============================================================
fig, ax = plt.subplots(figsize=(12, 7))

# 只保留前12个月
retention_plot = retention_rate.iloc[:, :13]

sns.heatmap(retention_plot, annot=True, fmt='.1%', cmap='YlGnBu',
            linewidths=0.5, ax=ax, cbar_kws={'label': '留存率'})

ax.set_title('用户同期群留存分析（Cohort Analysis）', fontsize=14, fontweight='bold', pad=20)
ax.set_xlabel('注册后第N个月', fontsize=12)
ax.set_ylabel('注册月份（同期群）', fontsize=12)

plt.tight_layout()
plt.savefig('cohort_analysis.png', dpi=150, bbox_inches='tight')
print("\n图表已保存: cohort_analysis.png")

# ============================================================
# 5. 分析结论
# ============================================================
print("\n" + "=" * 60)
print("同期群分析结论")
print("=" * 60)

# 首月留存
first_month_retention = retention_rate.iloc[:, 1].mean()
print(f"平均次月留存率: {first_month_retention*100:.1f}%")

# 3个月留存
if retention_rate.shape[1] > 3:
    third_month_retention = retention_rate.iloc[:, 3].mean()
    print(f"平均第3月留存率: {third_month_retention*100:.1f}%")

# 比较不同同期群的留存差异
print("\n各同期群次月留存率:")
for idx, row in retention_rate.iterrows():
    if 1 in row.index and not pd.isna(row[1]):
        print(f"  {idx}: {row[1]*100:.1f}%")

print("\n业务建议:")
print("  1. 对比不同月份同期群留存，判断产品迭代效果")
print("  2. 次月留存低 → 优化新用户引导流程(Onboarding)")
print("  3. 早期留存好但后期流失快 → 优化长期价值和内容生态")
