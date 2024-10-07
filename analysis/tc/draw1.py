import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 配置字体
config = {
    "font.family": 'serif',
    "font.size": 16,
    "mathtext.fontset": 'stix',
    "font.serif": ['KaiTi'],  # 仿宋的字体名称
}
plt.rcParams.update(config)

# 从CSV文件中读取数据
file_path = 'e:/master/dissertation/my-paper/thesis/experiment/data/tc_output.csv'  # 请根据实际路径调整
df = pd.read_csv(file_path)

# 获取每个节点的唯一值和操作速率的唯一值
nodes = df['nodes'].unique()
rates = df['rate'].unique()

# 设置柱状图的宽度
bar_width = 0.15
# 生成每个操作速率的 x 位置
x = np.arange(len(rates))

# 创建色彩列表
colors = plt.cm.Set1(np.linspace(0, 1, len(nodes)))

# 创建图形
plt.figure(figsize=(12, 6))

# 逐个节点绘制柱状图和折线图
for i, node in enumerate(nodes):
    subset = df[df['nodes'] == node]
    
    # 使用相同颜色绘制柱状图
    plt.bar(x + i * bar_width, subset['throughput'], width=bar_width, label=f'节点数量 = {node}', 
            color=colors[i], alpha=0.5)
    
    # 绘制折线图，使用相同颜色
    plt.plot(x + i * bar_width, subset['throughput'], marker='o', markersize=5, color=colors[i])

# 设置横坐标为操作速率
plt.xticks(x + bar_width * (len(nodes) - 1) / 2, rates)
# 添加图表标签
plt.xlabel('发送速率')
plt.ylabel('吞吐量 (TPS)')

# 只展示柱状图的图例
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.grid()
plt.tight_layout()
plt.show()
