import csv

# 读取数据
file_path = 'e:/master/dissertation/my-paper/thesis/experiment/data/all.csv'
throughput_data = {}

with open(file_path, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        nodes = row['nodes']
        operation = row['operation']
        throughput = float(row['throughput'])

        if nodes not in throughput_data:
            throughput_data[nodes] = {}

        if operation not in throughput_data[nodes]:
            throughput_data[nodes][operation] = []

        throughput_data[nodes][operation].append(throughput)

# 打印结果
for nodes, operations in throughput_data.items():
    print(f"nodes_{nodes}:")
    for operation, throughputs in operations.items():
        print(type(throughputs))
        print(f"  {operation}: {throughputs}")
