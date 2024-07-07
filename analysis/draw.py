import matplotlib.pyplot as plt
import numpy as np

# 设置字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 示例数据，每个x值对应多个y值
data = {
    3: [2.865350690914404,2.874592976976877,2.8767461422793006,2.871187378440057,2.867621686636091],
    5: [4.613976072304203,4.577917409694694,4.674592767914419,4.6139422129899055,4.571544234716077],
    7: [6.164907357757317,6.0778026705521935,5.954024712872333,6.031215774412188,5.949402184730541],
    9: [7.037869973702897,7.058706359985067,6.857416427493757,7.039967147575413,6.842122086790951],
    11: [7.385221853798464,7.473127655219645,7.576611129043865,7.503442652309791,7.333824457394428],
    13: [7.452836535268051,7.31016990054229,7.3281371211815785,7.609285989497077,7.640906350476669],
    15: [7.4342151980949795,7.385815415250746,7.277742938342938,7.287409396477116,7.185674739404479],
    17: [7.221962254213898,7.474821756371565,7.255027442664934,7.600786006435312,7.283214215399693],
    19: [7.371912615794147,7.244858069949539,7.426931226344773,7.298075622631987,7.213772345530596],
    21: [7.349980250437692,7.330995569232594,7.328111759564009,7.313456897222892,7.397157373664713]
}

# 计算每个x值对应的y值的平均值和标准差
x = list(data.keys())
y = [np.mean(values) for values in data.values()]
y_error = [np.std(values) for values in data.values()]

# 计算延迟
latency = [1000 / mean for mean in y]

# 计算延迟的标准差
latency_error = [1000 * std / (mean ** 2) for std, mean in zip(y_error, y)]

# 创建图形
fig, ax1 = plt.subplots(figsize=(8, 6))

# 绘制带有误差线的吞吐量折线图
ax1.errorbar(x, y, yerr=y_error, capsize=5, elinewidth=1, markeredgewidth=1, label='吞吐量', color='blue', markersize=5)
ax1.set_xlabel('发送速率（条/秒）')
ax1.set_ylabel('吞吐量（交易数/秒）', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

# 添加每个数据点的具体数值，并向上偏移
offset = 0.1  # 调整这个值来改变偏移量
for i, j in zip(x, y):
    ax1.text(i, j + offset + 0.15, f'{j:.2f}', ha='center', va='top', color='blue')

# 创建第二个y轴
ax2 = ax1.twinx()

# 绘制带有误差线的延迟折线图
ax2.errorbar(x, latency, yerr=latency_error, capsize=5, elinewidth=1, markeredgewidth=1, label='延迟', color='green', markersize=5)
ax2.set_ylabel('延迟（秒）', color='green')
ax2.tick_params(axis='y', labelcolor='green')

# 添加每个延迟数据点的具体数值，并向下偏移
for i, j in zip(x, latency):
    ax2.text(i, j - offset - 5, f'{j:.2f}', ha='center', va='top', color='green')

ax1.grid(True, linestyle='--')
ax2.grid(True, linestyle='--')
# 添加标题
plt.title('PBFT算法下不同发送速率下的吞吐量和延迟')

# 显示图例
fig.legend(loc='upper right')

# 显示图形
plt.show()
