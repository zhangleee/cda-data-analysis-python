# -*- coding: utf-8 -*-
"""
4.3 流程挖掘 - PM4Py实战

知识点说明：
使用PM4Py库进行业务流程挖掘，从事件日志中发现流程模型、分析瓶颈。

本文件由CDA教材ipynb转换而来，补充了详细中文注释以帮助理解。
"""

import warnings
warnings.filterwarnings("ignore")


############################################################
# # 模板9-流程挖掘
############################################################


############################################################
# # 1、导入IEEE XES格式数据
############################################################

# --- 代码块 3 ---
##导入IEEE XES格式数据
#IEEE XES是一种存储日志数据的标准格式。
from pm4py.objects.log.importer.xes import importer as xes_importer

log = xes_importer.apply('./running-example.xes')
print(log)

# --- 代码块 6 ---
print('The first trace in the log: \n', log[0])
print('-' * 80)
print('The first event of the first trace: \n', log[0][0])

# --- 代码块 7 ---
log[0:2:2][:3]

# --- 代码块 8 ---
print(type(log))
print(type(log[0]))
print(type(log[0][0]))

# --- 代码块 9 ---
print('Length of the log is %d' %(len(log)))
print('Length of the first trace is %d' %(len(log[0])))
print('Length of the first event is %d' %(len(log[0][0])))

# --- 代码块 10 ---
# 导出XES文件
from pm4py.objects.log.exporter.xes import exporter as xes_exporter
xes_exporter.apply(log, "./exportedLog.xes")


############################################################
# # 2、流程发现和流程监控
############################################################


############################################################
# # Directly-Follows Graph和流程监控的演示
############################################################

# --- 代码块 13 ---
from pm4py.algo.discovery.dfg import algorithm as dfg_discovery
from pm4py.visualization.dfg import visualizer as dfg_visualization

dfg = dfg_discovery.apply(log)
gviz = dfg_visualization.apply(dfg, log=log, variant=dfg_visualization.Variants.FREQUENCY)
dfg_visualization.view(gviz)

# --- 代码块 14 ---
#添加流程转换耗时信息
from pm4py.algo.discovery.dfg import algorithm as dfg_discovery
from pm4py.visualization.dfg import visualizer as dfg_visualization

dfg = dfg_discovery.apply(log, variant=dfg_discovery.Variants.PERFORMANCE)
gviz = dfg_visualization.apply(dfg, log=log, variant=dfg_visualization.Variants.PERFORMANCE)
dfg_visualization.view(gviz)
