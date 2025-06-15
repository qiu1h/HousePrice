import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 加载数据
train = pd.read_csv('data/train.csv')
test = pd.read_csv('data/test.csv')

# print("训练集维度:", train.shape)
# print("测试集维度:", test.shape)

# 原始分布
sns.histplot(train['SalePrice'], kde=True)
plt.title("原始 SalePrice 分布")
plt.show()

# 对数变换后
log_price = np.log1p(train['SalePrice'])
sns.histplot(log_price, kde=True)
plt.title("对数变换后的 SalePrice 分布")
plt.show()

"""
为什么要对目标值做对数变换？
🎯 原因 1：目标变量分布严重右偏（偏态分布）
在房价预测任务中，原始的 SalePrice 常常是这样的：
    大多数房子价格集中在一个较低区间（如 100k–200k）
    少数豪宅价格非常高（>500k 甚至 1M）
    导致数据右偏（Right Skewed）
➡ 这种分布对线性模型不友好，会违背“误差服从正态分布”的假设。

🎯 原因 2：提升模型线性可拟合性
线性回归模型本质是拟合 Y = bX + e 形式
但房价往往是非线性增长的，比如面积每增加一倍，价格不一定翻倍
对 SalePrice 做对数变换可以让目标更接近线性，模型更好拟合

🎯 原因 3：缩小极值差距，抑制异常值影响
原始房价中，豪宅会有极端值（如 $1,000,000），拉高均值，影响损失函数（如 MSE）
对数变换能“压缩”大值的幅度，使模型更关注主流房价区间
"""