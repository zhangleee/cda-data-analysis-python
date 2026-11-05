# CDA商业数据分析 Python 实战代码库

> 本项目将CDA（Certified Data Analyst）认证教材中的Excel/PowerBI案例全部迁移为Python实现，同时将教材中的ipynb代码整理为规范的.py文件，配套详细中文注释，适合学习和教学使用。

## 📚 项目背景

CDA数据分析师认证分为三个级别：
- **一级**：商业数据分析（Excel/PowerBI为主）
- **二级**：量化策略分析（Python统计分析为主）
- **三级**：敏捷数据挖掘（机器学习建模为主）

本项目完成了老师布置的三项任务：
1. ✅ 将教材中Power BI/Excel实现的案例，理解业务内涵后迁移为Python实现
2. ✅ 将教材中已有的Python代码（ipynb文件）整理为规范的.py文件，并补充详细注释
3. ✅ 全部代码开源上传至GitHub和Gitee

## 📁 项目结构

```
cda-business-data-analysis-python/
├── 01_cda_level1_business_analysis/     # CDA一级：商业数据分析
│   ├── ch02_analysis_methods/           # 第2章 数据分析方法
│   │   ├── boston_matrix/              # 波士顿矩阵分析
│   │   ├── rfm_model/                  # RFM用户价值模型
│   │   ├── cohort_analysis/            # 同期群留存分析
│   │   ├── funnel_chart/               # 销售漏斗分析
│   │   ├── correlation_analysis/        # 相关分析
│   │   └── six_analysis_methods/        # 六类基础分析方法
│   └── ch10_time_series_decomposition/  # 第10章 效应分解时间序列预测
│
├── 02_cda_level2_quantitative/          # CDA二级：量化策略分析
│   ├── ch04_data_processing/            # 第4章 Pandas数据处理与清洗
│   ├── ch05_data_visualization/         # 第5章 数据可视化
│   ├── ch06_data_preprocessing/         # 第6章 数据预处理
│   ├── ch07_dimension_reduction/        # 第7章 特征降维（PCA/因子分析）
│   ├── ch08_statistical_tests/          # 第8章 统计检验与回归
│   └── ch09_user_clustering/            # 第9章 用户分群（K-Means/层次聚类）
│
├── 03_cda_level3_data_mining/           # CDA三级：敏捷数据挖掘
│   ├── ch2_customer_value/              # 第2章 客户价值与用户画像
│   ├── ch3_fraud_detection/             # 第3章 申请反欺诈
│   ├── ch4_timeseries_optimization/     # 第4章 时间序列与运筹优化
│   ├── ch5_hyperparameter_tuning/       # 第5章 参数调优
│   ├── ch6_feature_engineering/         # 第6章 特征工程
│   └── ch7_imbalanced_data/             # 第7章 类别不平衡问题
│
└── 04_financial_data_mining/            # 金融数据分析案例实战
    ├── ch02_precision_marketing/        # 第2章 贷款精准营销模型
    ├── ch03_customer_segmentation/      # 第3章 多维客户细分
    ├── ch05_credit_A_card/             # 第5章 贷前信用风险A卡
    ├── ch06_credit_B_card/              # 第6章 贷中信用风险B卡
    ├── ch08_fraud_detection/            # 第8章 申请反欺诈模型
    ├── ch09_engineering/                # 第9章 算法工程化
    └── social_network/                  # 社交网络分析专题
```

## 🛠️ 环境依赖

```bash
pip install -r requirements.txt
```

主要依赖：
- Python 3.8+
- pandas, numpy
- matplotlib, seaborn, plotly
- scikit-learn
- statsmodels
- scipy
- mlxtend
- openpyxl

## 🚀 快速开始

1. 克隆仓库
```bash
git clone https://github.com/你的用户名/cda-business-data-analysis-python.git
cd cda-business-data-analysis-python
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 运行任意案例
```bash
python 01_cda_level1_business_analysis/ch02_analysis_methods/boston_matrix/boston_matrix.py
```

## 📖 知识点覆盖

### CDA一级（商业分析思维）
- ✅ 数据分析思维与方法体系
- ✅ 波士顿矩阵、RFM模型、用户忠诚度模型
- ✅ 同期群分析、漏斗图分析、相关分析
- ✅ 趋势/对比/构成/分布/关系/桑基图 六类基础分析
- ✅ PowerBI看板 → Python可视化迁移
- ✅ 效应分解时间序列预测

### CDA二级（量化分析）
- ✅ Pandas数据清洗与整合
- ✅ 描述性统计与数据可视化
- ✅ 抽样方法与数据预处理
- ✅ PCA主成分分析、因子分析
- ✅ 假设检验、方差分析、列联表检验
- ✅ 线性回归、逻辑回归
- ✅ K-Means聚类、层次聚类

### CDA三级（数据挖掘）
- ✅ 线性回归客户价值预测
- ✅ 逻辑回归用户响应预测（WOE/IV）
- ✅ 用户画像完整流程（PCA+因子+聚类）
- ✅ 关联规则Apriori、序列模式PrefixSpan
- ✅ 决策树、随机森林、XGBoost、LightGBM
- ✅ 孤立森林、LOF异常检测
- ✅ SARIMA时间序列、LSTM股价预测
- ✅ 运筹优化（线性/整数/二次规划）
- ✅ 流程挖掘PM4Py
- ✅ 超参数调优、Pipeline
- ✅ 特征工程、类别不平衡处理

### 金融实战
- ✅ 精准营销建模全流程
- ✅ 信用评分卡（A卡/B卡）
- ✅ Vintage分析
- ✅ 申请反欺诈网络分析
- ✅ 社交网络分析与社区发现

## ✨ 特色

1. **业务+技术双视角**：每个脚本开头都有业务内涵说明，不只是代码
2. **详细中文注释**：关键步骤都有解释，适合初学者
3. **可直接运行**：所有脚本都配有模拟数据，无需额外准备
4. **从Excel到Python**：理解原Excel/PowerBI的业务逻辑后用Python重新实现
5. **完整知识体系**：覆盖CDA一二三级全部核心知识点

## 📝 说明

- 本项目仅用于学习交流，数据均为模拟或教材配套数据
- 代码基于CDA教材案例整理，注释为补充说明
- 如有问题欢迎提Issue交流

## 📄 License

MIT License
