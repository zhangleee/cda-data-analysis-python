# -*- coding: utf-8 -*-
"""
波士顿矩阵（BCG Matrix）分析
============================
业务内涵：
    波士顿矩阵由波士顿咨询集团创立，通过「市场增长率」和「相对市场份额」两个维度，
    将企业业务/产品划分为四个象限：
    - 明星业务(Stars)：高增长、高份额 → 重点投入，保持领先
    - 现金牛业务(Cash Cows)：低增长、高份额 → 榨取现金流，维持稳定
    - 问题业务(Question Marks)：高增长、低份额 → 选择性投资，判断能否成为明星
    - 瘦狗业务(Dogs)：低增长、低份额 → 撤退或剥离

分析价值：
    帮助企业在有限资源下，合理分配营销和研发预算，决定哪些产品该加码、哪些该收割。
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # 非交互式后端，直接保存图片
import matplotlib.pyplot as plt
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# ============================================================
# 1. 模拟产品销售数据（与教材案例对应）
# ============================================================
# 实际业务中，这些数据来自销售系统导出的产品维度汇总
np.random.seed(42)
products = pd.DataFrame({
    '产品名称': ['产品A', '产品B', '产品C', '产品D', '产品E', '产品F', '产品G', '产品H'],
    '销售额': [1200, 980, 450, 320, 280, 150, 90, 60],       # 当期销售额（万元）
    '去年销售额': [1000, 1050, 380, 350, 220, 160, 100, 80],  # 去年同期销售额
    '最大竞品销售额': [800, 1200, 400, 500, 300, 200, 150, 120]  # 最大竞品销售额
})

# ============================================================
# 2. 计算两个核心维度
# ============================================================
# 维度1：市场增长率 = (当期销售额 - 去年销售额) / 去年销售额
products['市场增长率'] = (products['销售额'] - products['去年销售额']) / products['去年销售额']

# 维度2：相对市场份额 = 本产品销售额 / 最大竞品销售额
# （注意：相对市场份额 > 1 表示本产品领先竞品）
products['相对市场份额'] = products['销售额'] / products['最大竞品销售额']

print("=" * 60)
print("波士顿矩阵计算结果")
print("=" * 60)
print(products[['产品名称', '市场增长率', '相对市场份额']].to_string(index=False))

# ============================================================
# 3. 划分四象限（以市场增长率10%、相对市场份额1.0为分界线）
# ============================================================
# 分界线的选择取决于行业特征，这里用教材常用的经验值
growth_threshold = 0.10    # 市场增长率10%为高低分界
share_threshold = 1.0      # 相对市场份额1.0为高低分界

def classify_bcg(row):
    high_growth = row['市场增长率'] >= growth_threshold
    high_share = row['相对市场份额'] >= share_threshold
    if high_growth and high_share:
        return '明星业务(Stars)'
    elif high_growth and not high_share:
        return '问题业务(?)'
    elif not high_growth and high_share:
        return '现金牛业务(Cash Cows)'
    else:
        return '瘦狗业务(Dogs)'

products['业务类型'] = products.apply(classify_bcg, axis=1)

print("\n" + "=" * 60)
print("业务分类结果")
print("=" * 60)
print(products[['产品名称', '市场增长率', '相对市场份额', '业务类型']].to_string(index=False))

# ============================================================
# 4. 绘制波士顿矩阵图
# ============================================================
fig, ax = plt.subplots(figsize=(10, 8))

# 四象限背景色
ax.axhspan(growth_threshold, products['市场增长率'].max()*1.1,
           xmin=0.5, xmax=1, alpha=0.15, color='gold')
ax.axhspan(growth_threshold, products['市场增长率'].max()*1.1,
           xmin=0, xmax=0.5, alpha=0.15, color='orange')
ax.axhspan(0, growth_threshold,
           xmin=0.5, xmax=1, alpha=0.15, color='lightgreen')
ax.axhspan(0, growth_threshold,
           xmin=0, xmax=0.5, alpha=0.15, color='lightgray')

# 绘制散点（气泡大小=销售额）
for _, row in products.iterrows():
    size = row['销售额'] * 2
    ax.scatter(row['相对市场份额'], row['市场增长率'],
               s=size, alpha=0.7, edgecolors='black', linewidth=1)
    ax.annotate(row['产品名称'],
                (row['相对市场份额'], row['市场增长率']),
                ha='center', va='center', fontsize=10, fontweight='bold')

# 分界线
ax.axvline(x=share_threshold, color='black', linestyle='--', linewidth=1)
ax.axhline(y=growth_threshold, color='black', linestyle='--', linewidth=1)

# 象限标签
x_max = products['相对市场份额'].max() * 1.2
x_min = products['相对市场份额'].min() * 0.8
y_max = products['市场增长率'].max() * 1.2
y_min = products['市场增长率'].min() * 1.2

ax.text(x_max * 0.75, y_max * 0.85, '明星业务\n(高增长·高份额)\n→ 重点投资',
        ha='center', va='center', fontsize=12, fontweight='bold', color='#b8860b')
ax.text(x_min * 1.1, y_max * 0.85, '问题业务\n(高增长·低份额)\n→ 选择性投资',
        ha='center', va='center', fontsize=12, fontweight='bold', color='#ff8c00')
ax.text(x_max * 0.75, y_min * 0.5, '现金牛业务\n(低增长·高份额)\n→ 维持收割',
        ha='center', va='center', fontsize=12, fontweight='bold', color='#228b22')
ax.text(x_min * 1.1, y_min * 0.5, '瘦狗业务\n(低增长·低份额)\n→ 撤退剥离',
        ha='center', va='center', fontsize=12, fontweight='bold', color='gray')

ax.set_xlabel('相对市场份额（本产品 / 最大竞品）', fontsize=12)
ax.set_ylabel('市场增长率', fontsize=12)
ax.set_title('波士顿矩阵（BCG Matrix）产品分析', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('boston_matrix.png', dpi=150, bbox_inches='tight')
print("\n图表已保存: boston_matrix.png")

# ============================================================
# 5. 业务策略建议
# ============================================================
print("\n" + "=" * 60)
print("策略建议")
print("=" * 60)
for btype in products['业务类型'].unique():
    prods = products[products['业务类型'] == btype]['产品名称'].tolist()
    if '明星' in btype:
        print(f"【{btype}】{prods} → 加大投入，巩固市场领先地位，未来转变为现金牛")
    elif '现金牛' in btype:
        print(f"【{btype}】{prods} → 维持现有份额，最大化现金流，反哺明星和问题业务")
    elif '问题' in btype:
        print(f"【{btype}】{prods} → 评估增长潜力，有希望的加码投入，无希望的及时止损")
    else:
        print(f"【{btype}】{prods} → 逐步退出或剥离，释放资源到更有价值的业务")
