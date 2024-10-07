import pandas as pd
import matplotlib.pyplot as plt

# 配置字体
config = {
    "font.family": 'serif',
    "font.size": 16,
    "mathtext.fontset": 'stix',
    "font.serif": ['KaiTi'],  # 仿宋的字体名称
}
plt.rcParams.update(config)

# 定义不同的标记样式
markers = ['o', 's', 'D', '^', 'v', '>', '<', '*', 'X', 'P', '|']

fig, ax1 = plt.subplots(figsize=(10, 6))

# 读取CSV文件
data = pd.read_csv('e:/master/dissertation/my-paper/thesis/experiment/data/all.csv')

# 过滤条件：nodes为5
filtered_data = data[data['nodes'] == 13]

# 创建图例列表
handles = []

# 按照operation分组，并绘制不同的吞吐量折线
for i, operation in enumerate(filtered_data['operation'].unique()):
    operation_data = filtered_data[filtered_data['operation'] == operation]
    if operation == 'add':
        label = '添加策略的吞吐量'
    elif operation == 'delete':
        label = '删除策略的吞吐量'
    else:  # 检查操作
        label = '验证请求的吞吐量'
    # 绘制吞吐量
    line, = ax1.plot(operation_data['rate'], operation_data['throughput'], marker=markers[i % len(markers)], label=label)  # 用不同的标记样式
    handles.append(line)

# 设置第一个Y轴标签
ax1.set_xlabel('发送速率（TPS）')
ax1.set_ylabel('吞吐量（TPS）')
ax1.grid()

# 创建第二个Y轴
ax2 = ax1.twinx()
for i, operation in enumerate(filtered_data['operation'].unique()):
    operation_data = filtered_data[filtered_data['operation'] == operation]
    if operation == 'add':
        label = '添加策略的延迟'
    elif operation == 'delete':
        label = '删除策略的延迟'
    else:  # 检查操作
        label = '验证请求的延迟'
    # 绘制吞吐量
    line, = ax2.plot(operation_data['rate'], operation_data['latency'], marker=markers[i % len(markers)], linestyle='--', label=label)  # 用不同的标记样式
    handles.append(line)

# 设置第二个Y轴标签
ax2.set_ylabel('延迟（ms）')

# 合并图例，放到右侧
labels = [handle.get_label() for handle in handles]
ax1.legend(handles=handles, labels=labels, loc='center right', bbox_to_anchor=(1, 0.5))

# 导出为PDF文件
plt.savefig('e:/master/dissertation/my-paper/thesis/figures/节点数为13时区块链网络的吞吐量及延迟与发送速率关系.pdf', format='pdf', bbox_inches='tight')  # 保存图表为PDF

# # 显示图表
# plt.show()
