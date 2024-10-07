import pandas as pd
import matplotlib.pyplot as plt

# 配置字体
config = {
    "font.family": 'serif',
    "font.size": 12,
    "mathtext.fontset": 'stix',
    "font.serif": ['KaiTi'],
}
plt.rcParams.update(config)

# 读取数据
data = pd.read_csv(r'e:\master\dissertation\my-paper\thesis\experiment\data\all - 副本.csv')
operation_throughput = data[['operation', 'throughput']]

# 创建中文映射
operation_mapping = {
    'add': '添加策略',
    'delete': '删除策略',
    'check': '验证请求'
}

# 将英文操作类型转换为中文
operation_throughput['operation'] = operation_throughput['operation'].map(operation_mapping)

# 创建箱线图
plt.figure(figsize=(12, 6))

# 添加颜色
box = operation_throughput.boxplot(column='throughput', by='operation',
                                   patch_artist=True,
                                   boxprops=dict(facecolor='skyblue', color='black', linewidth=1.5), # 箱体颜色
                                   whiskerprops=dict(color='green', linewidth=1.5),  # 须颜色
                                   capprops=dict(color='blue', linewidth=1.5),        # 端点颜色
                                   medianprops=dict(color='red', linewidth=1.5))      # 中位线颜色

plt.title('')
plt.suptitle('')  # 移除默认的标题
plt.xlabel('')
plt.ylabel('吞吐量（TPS）')
# plt.xticks(rotation=30)  # 横坐标标签旋转以改善可读性
plt.grid(True)
print(operation_throughput)
plt.show()
