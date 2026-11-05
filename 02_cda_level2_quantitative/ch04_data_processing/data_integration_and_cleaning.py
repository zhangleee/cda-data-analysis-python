# -*- coding: utf-8 -*-
"""
第4章 数据处理（Pandas）- 数据整合与清洗

知识点说明：
本章系统讲解Pandas核心操作：数据读取（CSV/Excel）、行列索引、条件查询、横向连接(merge/join)、纵向合并(concat)、排序、分组汇总(groupby/agg)、透视表(pivot_table)、条件赋值、重复值处理、缺失值处理、异常值盖帽法处理、连续变量分箱(cut/qcut)。这是数据分析最基础也最重要的数据清洗环节。

本文件由CDA教材ipynb转换而来，补充了详细中文注释以帮助理解。
"""

import warnings
warnings.filterwarnings("ignore")


############################################################
# 1.1.1读取数据
############################################################

# --- 代码块 2 ---
import pandas as pd
csv = pd.read_csv('sample.csv')
csv

# --- 代码块 3 ---
csv = pd.read_csv('sample.csv',\
                   usecols=['id','name'],\
                   nrows=2) #读取'id'和'name'两列，仅读取前两行
csv

# --- 代码块 4 ---
csvs = pd.read_csv('data/big.csv',chunksize=900)
for i in csvs:
    print (i.shape)

# --- 代码块 5 ---
csvs = pd.read_csv('data/big.csv',chunksize=900)
dat = pd.concat(csvs,ignore_index=True)
dat.shape

# --- 代码块 6 ---
csv = pd.read_csv('sample.csv',
                  na_values='99999')
csv

# --- 代码块 7 ---
csv = pd.read_csv('sample.csv',
                  encoding='utf-8')
csv

# --- 代码块 8 ---
csv.to_csv('write.csv',encoding='utf-8',index=False)


############################################################
# 1.2.1 行列操作
############################################################

# --- 代码块 10 ---
import numpy as np
import pandas as pd
np.random.seed(0) #为保证代码每次运行都能得到相同的一组数据，设置随机数种子
sample = pd.DataFrame(np.random.randn(4,5)
                     ,columns=list("abcde")
                     )
sample

# --- 代码块 11 ---
sample['a']

# --- 代码块 12 ---
sample.iloc[:,0]

# --- 代码块 13 ---
sample.loc[:,"a"]

# --- 代码块 14 ---
sample[['a']]

# --- 代码块 15 ---
sample.loc[:1,:"b"]

# --- 代码块 16 ---
sample.iloc[0:2,0:2]

# --- 代码块 17 ---
sample['new_col'] = sample['a'] - sample['b']
sample

# --- 代码块 18 ---
sample.assign(new_col2 = sample['a'] - sample['b'],
                  new_col3 = sample['a'] + sample['b'])

# --- 代码块 19 ---
sample.drop(columns='a')

# --- 代码块 20 ---
sample.drop(columns=['a','b'])


############################################################
# 1.2.2 条件查询
############################################################

# --- 代码块 22 ---
sample =pd.DataFrame({'group':[1,1,1,2,1,2]
                      ,'name':['Bob','Lindy','Mark','Miki','Sully','Rose']
                      ,'score':[98,78,87,77,65,67]
                      ,})
sample

# --- 代码块 23 ---
sample.score > 70

# --- 代码块 24 ---
sample[sample.score > 70]

# --- 代码块 25 ---
sample[(sample.score > 70) & (sample.group ==1)] #且

# --- 代码块 26 ---
sample[~(sample.group ==1)] #非

# --- 代码块 27 ---
sample[(sample.group ==2) | (sample.group ==1)]

# --- 代码块 28 ---
sample.query('score > 90')

# --- 代码块 29 ---
sample.query('(group ==2) |(group == 1)')

# --- 代码块 30 ---
# sample[sample['score'].between(70,80),inclusive=True]
sample[sample['score'].between(70, 80, inclusive='both')]#Pandas 1.3.0 版本开始，inclusive 参数被修改为 inclusive='both'（或’neither’/‘left’/‘right’） 的字符串形式

# --- 代码块 31 ---
sample[sample['name'].isin(['Bob','Lindy'])]

# --- 代码块 32 ---
sample[sample['name'].str.contains('[M]+')]


############################################################
# 1.2.3 横向连接
############################################################

# --- 代码块 34 ---
df1 = pd.DataFrame({ 'col1':['a','b','c'],
                     'id':[1,2,3],
                   })
df2 = pd.DataFrame({ 'col2':['d','e'],
                    'id':[4,3],
                   })

# --- 代码块 35 ---
df1

# --- 代码块 36 ---
df2

# --- 代码块 37 ---
df1.merge(df2,how='inner',on='id')

# --- 代码块 38 ---
df1.merge(df2,how='inner',left_on='id',right_on='id')

# --- 代码块 39 ---
df1.merge(df2,how='left',on='id')

# --- 代码块 40 ---
df1.merge(df2,how='right',on='id')

# --- 代码块 41 ---
df1.merge(df2,how='outer',on='id')

# --- 代码块 42 ---
df1 = pd.DataFrame({'id1':[1,2,3],
                    'col1':['a','b','c']},
                  index = [1,2,3])
df2 = pd.DataFrame({'id2':[1,2,3],
                    'col2':['aa','bb','cc']},
                  index = [1,3,2])

# --- 代码块 43 ---
df1

# --- 代码块 44 ---
df2

# --- 代码块 45 ---
pd.concat([df1,df2],axis=1)

# --- 代码块 46 ---
df1.join(df2)


############################################################
# 1.2.4 纵向合并
############################################################

# --- 代码块 48 ---
df1 = pd.DataFrame({'id':[1,1,1,2,3,4,6],
                    'col':['a','a','b','c','v','e','q']})
df2 = pd.DataFrame({'id':[1,2,3,3,5],
                    'col':['x','y','z','v','w']})

# --- 代码块 49 ---
df1

# --- 代码块 50 ---
df2

# --- 代码块 51 ---
pd.concat([df1,df2],ignore_index=True,axis=0)

# --- 代码块 52 ---
pd.concat([df1,df2],ignore_index=True).drop_duplicates()

# --- 代码块 53 ---
df3 = df1.rename(columns = {'col':'new_col'})
df3

# --- 代码块 54 ---
pd.concat([df1,df3],ignore_index=True).drop_duplicates()


############################################################
# 1.2.5 排序
############################################################

# --- 代码块 56 ---
sample=pd.DataFrame({'group':[1,1,1,2,1,2],
                    'name':['Bob','Lindy','Mark','Miki','Sully','Rose'],
                    'score':[98,78,87,77,77,np.nan],
                    })
sample

# --- 代码块 57 ---
sample.sort_values('score',ascending=False,na_position='last')

# --- 代码块 58 ---
sample.sort_values(['group','score'])


############################################################
# 1.2.6 分组汇总
############################################################

# --- 代码块 60 ---
sample = pd.DataFrame({"name":['Bob','Lindy','Mark','Miki','Sully','Rose']
                        ,"class":[1,1,1,2,1,2]
                        ,"grade":[1,1,1,2,2,2]
                        ,"chinese":[88,78,86,56,77,54]
                        ,"math":[98,78,87,77,77,np.nan]
                        })
sample

# --- 代码块 61 ---
sample.groupby('grade')[['math']].max()

# --- 代码块 62 ---
sample.groupby(['grade','class'])[['math']].mean()

# --- 代码块 63 ---
sample.groupby(['grade']) [['math','chinese']].mean()

# --- 代码块 64 ---
sample.groupby('class')['math'].agg(['mean','min','max'])

# --- 代码块 65 ---
df = sample.groupby(['grade','class']) [['math','chinese']].agg(['min','max'])
df

# --- 代码块 66 ---
df['math']['min']

# --- 代码块 67 ---
df.loc[:,('math','min')]

# --- 代码块 68 ---
df.loc[(2,2),('math','min')]


############################################################
# 1.2.7 拆分列
############################################################

# --- 代码块 70 ---
table = pd.DataFrame({ 'Monetary':[3608,420,1894,3503,4567],
                        'cust_id':[10001,10001,10002,10002,10003],
                        'type':['Normal','Special_offer',\
                        'Normal','Special_offer','Special_offer']
                     })
table

# --- 代码块 71 ---
pd.pivot_table(table,index='cust_id',columns='type',values='Monetary')

# --- 代码块 72 ---
pd.pivot_table(table,index='cust_id',columns='type',values='Monetary',
        fill_value=0,aggfunc='sum')


############################################################
# 1.2.8 赋值与条件赋值
############################################################

# --- 代码块 74 ---
sample = pd.DataFrame({'name':['Bob','Lindy','Mark',
        'Miki','Sully','Rose'],
        'score':[99,78,999,77,77,np.nan],
        'group':[1,1,1,2,1,2],})
sample

# --- 代码块 75 ---
sample.score.replace(999,np.nan)

# --- 代码块 76 ---
sample.replace({'score':{999:np.nan},
                'name':{'Bob':np.nan}})

# --- 代码块 77 ---
sample

# --- 代码块 78 ---
def transform(row):
    if row['group'] == 1:
        return ('class1')
    elif row['group'] == 2:
        return ('class2')  

sample.apply(transform,axis=1)

# --- 代码块 79 ---
sample.assign(class_n = sample.apply(transform,axis=1))

# --- 代码块 80 ---
sample = sample.copy()
sample.loc[sample.group==1,'class_n']='class1'
sample.loc[sample.group==2,'class_n']='class2'
sample


############################################################
# 1.3.1 重复值处理
############################################################

# --- 代码块 82 ---
sample = pd.DataFrame({'group':[1,1,1,2,1,2],
                        'id':[1,1,1,3,4,5],
                       'name':['Bob','Bob','Mark','Miki','Sully','Rose'],
                       'score':[99,99,87,77,77,np.nan],
                       })
sample

# --- 代码块 83 ---
sample[sample.duplicated()]

# --- 代码块 84 ---
sample.drop_duplicates()

# --- 代码块 85 ---
sample.drop_duplicates('id')


############################################################
# 1.3.2 缺失值处理
############################################################

# --- 代码块 87 ---
sample = pd.DataFrame({'group':[1,1,np.nan,2,1,np.nan],
                        'id':[1,1,1,3,4,np.nan],
                       'name':['Bob','Bob','Mark','Miki','Sully',np.nan],
                       'score':[99,np.nan,87,77,77,np.nan],
                       })
sample

# --- 代码块 88 ---
sample.apply(lambda col:sum(col.isnull())/col.size)

# --- 代码块 89 ---
sample.score.fillna(sample.score.mean())

# --- 代码块 90 ---
sample.score.fillna(sample.score.median())

# --- 代码块 91 ---
sample.score.isnull()

# --- 代码块 92 ---
sample.score.isnull().apply(int)


############################################################
# 1.3.3 噪声值处理
############################################################

# --- 代码块 94 ---
def cap(x,quantile=[0.01,0.99]):
    """盖帽法处理异常值
    Args：
        x：pd.Series列，连续变量
        quantile：指定盖帽法的上下分位数范围
    """

# 生成分位数
    Q01,Q99=x.quantile(quantile).values.tolist()

# 替换异常值为指定的分位数
    if Q01 > x.min():
        x = x.copy()
        x.loc[x<Q01] = Q01

    if Q99 < x.max():
        x = x.copy()
        x.loc[x>Q99] = Q99

    return(x)

# --- 代码块 95 ---
sample = pd.DataFrame({'normal':np.random.randn(1000)})
sample.hist(bins=50)

# --- 代码块 96 ---
new = sample.apply(cap,quantile=[0.01,0.99])
new.hist(bins=50)

# --- 代码块 97 ---
np.random.seed(0)
sample =pd.DataFrame({'normal':np.random.randn(10)})
sample

# --- 代码块 98 ---
pd.cut(sample.normal,5)

# --- 代码块 99 ---
pd.cut(sample.normal,bins=5,labels=[1,2,3,4,5])

# --- 代码块 100 ---
pd.cut(sample.normal,bins=2,labels=['bad','good'])

# --- 代码块 101 ---
sample.normal.quantile([0,0.5,1])

# --- 代码块 102 ---
pd.cut(sample.normal,bins=sample.normal.quantile([0,0.5,1]),
 include_lowest=True)

# --- 代码块 103 ---
pd.cut(sample.normal,bins=sample.normal.quantile([0,0.5,1]),labels=['bad','good'],include_lowest=True)
