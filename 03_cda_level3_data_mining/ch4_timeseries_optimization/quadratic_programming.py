# -*- coding: utf-8 -*-
"""
4.2.3 运筹优化 - 二次规划

知识点说明：
二次规划用于求解二次目标函数在线性约束下的最优解，常见于投资组合优化。

本文件由CDA教材ipynb转换而来，补充了详细中文注释以帮助理解。
"""

import warnings
warnings.filterwarnings("ignore")


############################################################
# ### 二次规划
############################################################

# --- 代码块 2 ---
import cplex

op = cplex.Cplex()
op.read("qp1.lp")
op.solve()
# 输出结果
print(op.solution.get_objective_value())
print(op.solution.get_values())
