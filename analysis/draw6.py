import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 读取CSV文件
file_path = r'e:\master\dissertation\my-paper\thesis\experiment\data\average_cpu_mem.csv'
data = pd.read_csv(file_path)

# 提取需要的列
data_filtered = data[['rate', 'avg_cpu']]

# 打印前几行以检查数据
print(data_filtered.head())

# 计算相关系数
correlation = data_filtered.corr().iloc[0, 1]
print(f'Rate和avg_mem之间的相关系数: {correlation}')

# 绘制散点图并显示回归线
plt.figure(figsize=(10, 6))
sns.regplot(x='rate', y='avg_cpu', data=data_filtered)
plt.title('Rate vs Avg Mem')
plt.xlabel('Rate')
plt.ylabel('Average Memory Usage (Avg Mem)')
plt.grid()
plt.show()
