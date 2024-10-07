import pandas as pd
import csv
import matplotlib.pyplot as plt


data = pd.read_csv('e:/master/dissertation/my-paper/thesis/experiment/data/all.csv')
for index, row in data.iterrows():
    node = row['nodes']
    operation = row['operation']
    rate = row['rate']
    start_time = row['start_time']
    end_time = row['end_time']
    if operation == 'check':
        cpu_file_path = 'e:/master/dissertation/my-paper/thesis/experiment/data/pbft/' + str(node) + 'node' + '/check_' + str(rate) + 'rate_0_cpu.csv'
        mem_file_path = 'e:/master/dissertation/my-paper/thesis/experiment/data/pbft/' + str(node) + 'node' + '/check_' + str(rate) + 'rate_0_mem.csv'
    else:
        cpu_file_path = 'e:/master/dissertation/my-paper/thesis/experiment/data/pbft/' + str(node) + 'node' + '/add+delete_' + str(rate) + 'rate_0_cpu.csv'
        mem_file_path = 'e:/master/dissertation/my-paper/thesis/experiment/data/pbft/' + str(node) + 'node' + '/add+delete_' + str(rate) + 'rate_0_mem.csv'
    cpu_data = pd.read_csv(cpu_file_path)
    mem_data = pd.read_csv(mem_file_path)
    filtered_cpu_data = cpu_data[(cpu_data['time'] >= start_time) & (cpu_data['time'] <= end_time)]
    filtered_mem_data = mem_data[(mem_data['time'] >= start_time) & (mem_data['time'] <= end_time)]
    # filtered_mem_data的vmalloc_used列的单位是字节，需要先去掉最后一个字符，转换为MB
    filtered_mem_data['vmalloc_used'] = filtered_mem_data['vmalloc_used'].apply(lambda x: float(x[:-1])/1024/1024)
    # 画出filtered_cpu_data的箱线图
    # filtered_cpu_data.boxplot(column=['usage_user'], by='host')
    # 画出filtered_mem_data的箱线图
    # filtered_mem_data.boxplot(column=['vmalloc_used'], by='host')
    # plt.show()
    # 计算filtered_cpu_data的不同host的平均值
    avg_cpu = filtered_cpu_data.groupby(['host']).mean()
    # 计算filtered_mem_data的不同host的平均值
    avg_mem = filtered_mem_data.groupby(['host']).mean()
    # 创建新的csv文件，标题是node,operation,rate,host,avg_cpu,avg_cpu
    with open('e:/master/dissertation/my-paper/thesis/experiment/data/average_cpu_mem.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # 如果文件是空的，则写入标题
        if csvfile.tell() == 0:  # 判断是否是空文件 
            writer.writerow(['node', 'operation', 'rate', 'host', 'avg_cpu', 'avg_mem'])
        for host in avg_cpu.index:
            writer.writerow([node, operation, rate, host, avg_cpu.loc[host]['usage_user'], avg_mem.loc[host]['vmalloc_used']])
