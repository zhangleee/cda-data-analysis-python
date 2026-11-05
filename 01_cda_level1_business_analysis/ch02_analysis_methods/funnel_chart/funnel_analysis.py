# -*- coding: utf-8 -*-
"""
销售漏斗图分析
==============
业务内涵：
    漏斗分析用于追踪用户从进入到转化的完整路径，
    发现哪个环节流失最多，从而针对性优化。
    常见于电商转化、销售线索、用户注册等场景。

核心指标：
    - 环节转化率 = 当前环节用户数 / 上一环节用户数
    - 总体转化率 = 当前环节用户数 / 第一环节用户数
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# ============================================================
# 1. 销售漏斗数据（与教材案例对应）
# ============================================================
funnel_data = pd.DataFrame({
    '阶段': ['潜在客户', '初步接触', '产生意向', '需求明确', '商务谈判', '成交签约'],
    '用户数': [10000, 7200, 4500, 2800, 1500, 600]
})

print("=" * 60)
print("销售漏斗原始数据")
print("=" * 60)
print(funnel_data.to_string(index=False))

# ============================================================
# 2. 计算转化率
# ============================================================
funnel_data['环节转化率'] = funnel_data['用户数'] / funnel_data['用户数'].shift(1)
funnel_data['总体转化率'] = funnel_data['用户数'] / funnel_data['用户数'].iloc[0]

# 第一行的环节转化率为100%
funnel_data.loc[0, '环节转化率'] = 1.0

print("\n" + "=" * 60)
print("漏斗转化率分析")
print("=" * 60)
print(funnel_data.to_string(index=False))

# 找出流失最严重的环节
funnel_data['流失人数'] = funnel_data['用户数'].shift(1) - funnel_data['用户数']
funnel_data['流失人数'].iloc[0] = 0
worst_stage = funnel_data.loc[funnel_data['流失人数'].idxmax()]
print(f"\n流失最严重环节: {worst_stage['阶段']}，流失 {int(worst_stage['流失人数'])} 人")

# ============================================================
# 3. 绘制漏斗图
# ============================================================
fig, ax = plt.subplots(figsize=(10, 7))

# 颜色渐变
colors = ['#2196F3', '#03A9F4', '#00BCD4', '#009688', '#4CAF50', '#8BC34A']

y_pos = np.arange(len(funnel_data))[::-1]  # 倒序，最上面是第一阶段
max_width = funnel_data['用户数'].max()

for i, (_, row) in enumerate(funnel_data.iterrows()):
    width = row['用户数'] / max_width
    left = (1 - width) / 2  # 居中
    ax.barh(y_pos[i], width, left=left, height=0.8,
            color=colors[i], edgecolor='white', linewidth=2)
    # 标签
    ax.text(0.5, y_pos[i],
            f"{row['阶段']}: {row['用户数']:,}人 ({row['总体转化率']*100:.1f}%)",
            ha='center', va='center', fontsize=11, fontweight='bold', color='white')

# 标注环节转化率
for i in range(1, len(funnel_data)):
    conv_rate = funnel_data['环节转化率'].iloc[i]
    ax.text(1.02, y_pos[i], f"环节转化率: {conv_rate*100:.1f}%",
            va='center', fontsize=10, color='#666')

ax.set_xlim(0, 1.3)
ax.set_yticks([])
ax.set_xticks([])
ax.set_title('销售转化漏斗分析', fontsize=16, fontweight='bold', pad=20)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

plt.tight_layout()
plt.savefig('funnel_analysis.png', dpi=150, bbox_inches='tight')
print("\n图表已保存: funnel_analysis.png")

# ============================================================
# 4. 优化建议
# ============================================================
print("\n" + "=" * 60)
print("漏斗优化建议")
print("=" * 60)
print(f"整体转化率: {funnel_data['总体转化率'].iloc[-1]*100:.2f}%")
print(f"平均环节转化率: {funnel_data['环节转化率'].mean()*100:.1f}%")
print(f"\n重点优化环节: {worst_stage['阶段']}")
print("  建议: 分析该环节流失原因，优化产品/话术/流程")
