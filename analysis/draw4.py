import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# 配置字体
config = {
    "font.family": 'serif',
    "font.size": 16,
    "mathtext.fontset": 'stix',
    "font.serif": ['KaiTi'],
}
plt.rcParams.update(config)
# 读取 CSV 文件
file_path = r'e:\master\dissertation\my-paper\thesis\experiment\data\average_cpu_mem.csv'
data = pd.read_csv(file_path)

# 数据清洗：去掉空值
data.dropna(inplace=True)

# 转换类别变量为数值，便于计算相关性
data['node'] = data['node'].astype('category').cat.codes
data['operation'] = data['operation'].astype('category').cat.codes
data['host'] = data['host'].astype('category').cat.codes

# 计算相关性矩阵
correlation_matrix = data[['node', 'operation', 'rate', 'host', 'avg_cpu', 'avg_mem']].corr()
# 可视化相关性矩阵
plt.figure(figsize=(10, 10))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', square=True)
plt.show()
