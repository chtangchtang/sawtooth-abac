import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 读取CSV文件
file_path = r'e:\master\dissertation\my-paper\thesis\experiment\data\average_cpu_mem.csv'
data = pd.read_csv(file_path)

# 设置绘图风格
sns.set_theme(style="whitegrid", palette="Set3", font='KaiTi')

# 绘制箱线图，箱体颜色保持默认，所有线条为黑色
plt.figure(figsize=(12, 6))
sns.boxplot(x='rate', y='avg_mem', data=data, 
            boxprops=dict(edgecolor='black', linewidth=1.2), # 箱体颜色
            whiskerprops=dict(color='green', linewidth=1.2),  # 须颜色
            capprops=dict(color='darkblue', linewidth=1.2),        # 端点颜色
            medianprops=dict(color='darkorange', linewidth=1.2),
            flierprops={'marker':'o', 'markeredgecolor':'black', 'markerfacecolor':'none', 'linewidth': 1.2})

# 添加标签
plt.xlabel('发送速率', fontsize=20)
plt.ylabel('平均内存消耗（MB）', fontsize=20)
plt.grid(True)

# 显示图表
plt.show()
