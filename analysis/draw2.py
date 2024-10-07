import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
# 配置字体
config = {
    "font.family": 'serif',
    "font.size": 16,
    "mathtext.fontset": 'stix',
    "font.serif": ['KaiTi'],  # 仿宋的字体名称
}
plt.rcParams.update(config)
# 读取数据
data = """
5,add,8.100310383519155
5,delete,7.976501428928582
5,check,8.109938577470063
7,add,6.712920767412211
7,delete,6.798201298598568
7,check,6.389326908074629
9,add,4.889769075684982
9,delete,5.172964442491471
9,check,4.7822868798301545
11,check,3.964956108704591
11,add,3.92318488819312
11,delete,4.040376629327723
13,check,3.8169816373162555
13,add,3.808190814862564
13,delete,3.808957157686994
"""

# 将数据转换为DataFrame
from io import StringIO
df = pd.read_csv(StringIO(data), header=None, names=['Value', 'Action', 'Throughput'])

# 透视数据
pivot_df = df.pivot(index='Value', columns='Action', values='Throughput').fillna(0)

# 创建柱状图
plt.figure(figsize=(10, 6))
bar_width = 0.25
x = np.arange(len(pivot_df))

# 定义不同的标记样式和连线颜色
markers = ['o', 's', '^']  # 圆形、方形和三角形
line_colors = ['red', 'blue', 'yellow']  # 不同颜色用作连线颜色

# 绘制柱状图和连线
for idx, action in enumerate(pivot_df.columns):
    if action == 'check':
        label = '验证请求'
    elif action == 'add':
        label = '添加策略'
    else:
        label = '删除策略'
    bars = plt.bar(x + idx * bar_width, pivot_df[action], width=bar_width, label=label)
    
    # 在每个柱子上方显示数值
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom', fontsize=12)

    # 连接同一颜色的柱子顶部坐标，使用不同的标记和颜色
    plt.plot(x + idx * bar_width, pivot_df[action], marker=markers[idx], 
             linestyle='--', markersize=8, color=line_colors[idx])

# 设置X轴标签
plt.xticks(x + bar_width, pivot_df.index)

# 添加标签
plt.xlabel('节点数量（个）')
plt.ylabel('预测的吞吐量的阈值（TPS）')
plt.legend()

# 显示图形
plt.tight_layout()
plt.savefig('e:/master/dissertation/my-paper/thesis/figures/预测的吞吐量的阈值.pdf', format='pdf', bbox_inches='tight')
plt.show()
