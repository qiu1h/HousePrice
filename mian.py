import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 加载数据
train = pd.read_csv('data/train.csv')
test = pd.read_csv('data/test.csv')

print("训练集维度:", train.shape)
print("测试集维度:", test.shape)

# 目标变量：SalePrice 分布
sns.histplot(train['SalePrice'], kde=True)
plt.title("SalePrice 分布")
plt.show()

# 目标值对数变换（处理偏态分布）
train['SalePrice'] = np.log1p(train['SalePrice'])

# 保存 SalePrice
y = train['SalePrice']

# 合并特征部分，统一处理
train_ID = train['Id']
test_ID = test['Id']
train.drop(['Id', 'SalePrice'], axis=1, inplace=True)
test.drop(['Id'], axis=1, inplace=True)

all_data = pd.concat([train, test], axis=0)

# 统计缺失值
na_total = all_data.isnull().sum()
na_cols = na_total[na_total > 0].sort_values(ascending=False)
print("缺失值最多的列：\n", na_cols)

# 示例：根据列类型选择不同填补方式
# 数值型填 0
num_cols = all_data.select_dtypes(include=[np.number]).columns
all_data[num_cols] = all_data[num_cols].fillna(0)

# 类别型填 "None"
cat_cols = all_data.select_dtypes(include=["object"]).columns
all_data[cat_cols] = all_data[cat_cols].fillna("None")

# One-Hot 编码所有分类特征
all_data = pd.get_dummies(all_data)

print("编码后总维度：", all_data.shape)

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
all_data_scaled = scaler.fit_transform(all_data)

# 拆分回训练集与测试集
X = all_data_scaled[:train.shape[0]]
X_test = all_data_scaled[train.shape[0]:]

from sklearn.linear_model import LassoCV
from sklearn.model_selection import cross_val_score

# 定义交叉验证函数（RMSE）
def rmse_cv(model):
    rmse = -cross_val_score(model, X, y, scoring="neg_root_mean_squared_error", cv=5)
    return rmse

# 训练 Lasso
lasso = LassoCV(alphas=np.logspace(-4, 0.1, 50), cv=5)
lasso.fit(X, y)

print("最优 alpha:", lasso.alpha_)
print("交叉验证 RMSE:", rmse_cv(lasso).mean())

# 预测（注意目标变量已 log 过）
y_pred_log = lasso.predict(X_test)
y_pred = np.expm1(y_pred_log)  # 还原 SalePrice

# 生成提交文件
submission = pd.DataFrame({
    'Id': test_ID,
    'SalePrice': y_pred
})
submission.to_csv("submission_lasso.csv", index=False)
