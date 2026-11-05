# -*- coding: utf-8 -*-
"""
相关分析（Correlation Analysis）
================================
业务内涵：
    相关分析用于衡量两个变量之间的线性关系强度和方向。
    常见指标：
    - 皮尔逊相关系数(Pearson)：衡量线性相关，取值[-1, 1]
        r > 0 正相关，r < 0 负相关，|r|越接近1相关性越强
    - 斯皮尔曼相关系数(Spearman)：衡量单调关系，不要求线性，对异常值更稳健

应用场景：
    - 探索性分析：哪些因素与目标变量相关？
    - 特征工程：筛选与因变量相关的自变量
    - 多重共线性检测：自变量之间相关性太高会影响回归模型
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# ============================================================
# 1. 模拟数据（与教材案例对应：广告投入 vs 销售额）
# ============================================================
np.random.seed(42)
n = 100

# 广告投入与销售额的正相关关系
ad_spend = np.random.uniform(100, 500, n)  # 广告投入（万元）
# 销售额 = 基础 + 广告效应 + 噪声
sales = 200 + 1.2 * ad_spend + np.random.normal(0, 50, n)

df = pd.DataFrame({
    '广告投入': ad_spend,
    '销售额': sales
})

print("=" * 60)
print("原始数据（前10条）")
print("=" * 60)
print(df.head(10).to_string(index=False))
print(f"\n数据量: {len(df)} 条")

# ============================================================
# 2. 计算相关系数
# ============================================================
# 皮尔逊相关系数
pearson_r, pearson_p = stats.pearsonr(df['广告投入'], df['销售额'])

# 斯皮尔曼相关系数
spearman_r, spearman_p = stats.spearmanr(df['广告投入'], df['销售额'])

print("\n" + "=" * 60)
print("相关系数计算结果")
print("=" * 60)
print(f"皮尔逊相关系数 r = {pearson_r:.4f}, p值 = {pearson_p:.2e}")
print(f"斯皮尔曼相关系数 ρ = {spearman_r:.4f}, p值 = {spearman_p:.2e}")

# 相关性强弱判断
def interpret_correlation(r):
    r = abs(r)
    if r >= 0.8:
        return '极强相关'
    elif r >= 0.6:
        return '强相关'
    elif r >= 0.4:
        return '中等程度相关'
    elif r >= 0.2:
        return '弱相关'
    else:
        return '极弱相关或无相关'

print(f"\n皮尔逊相关强度判断: {interpret_correlation(pearson_r)}")
print(f"统计显著性: {'显著(p<0.05)' if pearson_p < 0.05 else '不显著'}")

# ============================================================
# 3. 可视化
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# 散点图 + 回归线
sns.regplot(x='广告投入', y='销售额', data=df, ax=axes[0],
            scatter_kws={'alpha': 0.6, 's': 50},
            line_kws={'color': 'red', 'linewidth': 2})
axes[0].set_title(f'广告投入 vs 销售额 (Pearson r={pearson_r:.3f})',
                  fontsize=12, fontweight='bold')
axes[0].set_xlabel('广告投入（万元）')
axes[0].set_ylabel('销售额（万元）')
axes[0].grid(True, alpha=0.3)

# 相关系数热力图（多变量时）
# 模拟更多变量
df_multi = pd.DataFrame({
    '广告投入': ad_spend,
    '销售额': sales,
    '价格': np.random.uniform(50, 200, n),
    '客流量': ad_spend * 0.8 + np.random.normal(0, 30, n)
})

corr_matrix = df_multi.corr()
sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='coolwarm',
            center=0, square=True, ax=axes[1], linewidths=0.5)
axes[1].set_title('多变量相关系数矩阵', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('correlation_analysis.png', dpi=150, bbox_inches='tight')
print("\n图表已保存: correlation_analysis.png")
plt.show()

# ============================================================
# 4. 注意事项
# ============================================================
print("\n" + "=" * 60)
print("相关分析注意事项")
print("=" * 60)
print("""
1. 相关 ≠ 因果：
   两个变量相关，不代表一个导致另一个。可能存在第三方变量(混淆变量)。
   例如：冰淇淋销量和溺水死亡人数正相关，但真正原因是「夏天热」。

2. 线性相关的局限：
   皮尔逊相关只衡量线性关系。U型曲线等非线性关系，即使r接近0，
   两个变量也可能有很强的关联。

3. 异常值影响大：
   几个极端值会显著改变相关系数，建议结合散点图判断。

4. 样本量：
   小样本的相关系数不稳定，需要看p值判断统计显著性。
""")
