# -*- coding: utf-8 -*-
"""
2.4.2 交叉销售 - 序列模式（PrefixSpan）

知识点说明：
使用PrefixSpan算法挖掘客户购买银行产品的序列模式，发现产品推荐的时序规律。

本文件由CDA教材ipynb转换而来，补充了详细中文注释以帮助理解。
"""

import warnings
warnings.filterwarnings("ignore")


############################################################
# ### AprioriAll
############################################################

# --- 代码块 2 ---
import pandas as pd

data = pd.read_csv('bank_prod_order.csv', encoding='gbk')

# 按照订单编号与用户编号分组汇总
baskets = data.groupby(['OrderNumber', 'CSR_ID'])['PROD'].apply(list)
baskets.head()

# --- 代码块 3 ---
# 按照用户编号分组汇总
baskets = baskets.groupby(level=1).apply(list)
baskets.head()

# --- 代码块 4 ---
import sys
sys.path.append('./myscript')  # aprioriAll.py放在'./myscript'文件夹下
from aprioriAll import aprioriAll

patterns = aprioriAll(baskets, min_support=0.1)
patterns.head()


############################################################
# ### prefixspan算法
############################################################

# --- 代码块 6 ---
import sys

sys.path.append('./myscript')  # prefixspan.py放在'./myscript'下

from prefixspan import SquencePattern, prefixSpan

patterns = prefixSpan(SquencePattern([], 1e4), baskets, threshold=100)
for pattern in patterns:
    print(pattern.squence, "-> support:", pattern.support)
