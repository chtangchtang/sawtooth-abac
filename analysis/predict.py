import csv
import numpy as np
from scipy.optimize import fsolve


def predict_throughput(x, y):
    # 输入的横坐标和纵坐标
    x = np.array(x)  # 用实际数据替换
    y = np.array(y)  # 用实际数据替换
    # 多项式拟合
    degree = 7  # 可以根据实际情况选择多项式的阶数
    coefficients = np.polyfit(x, y, degree)
    polynomial = np.poly1d(coefficients)
    # 求导
    def derivative(x):
        return np.polyder(polynomial)(x)
    # 寻找导数为零的点，即极值点
    derivative_eq = lambda x: derivative(x)
    initial_guesses = np.linspace(min(x), max(x), 100)  # 生成初始猜测
    critical_points = []
    for guess in initial_guesses:
        root = fsolve(derivative_eq, guess)
        if root not in critical_points:
            critical_points.append(root[0])
    # 计算极值对应的y值
    extreme_values = [(cp, polynomial(cp)) for cp in critical_points]
    # 找到最大值
    max_value_point = max(extreme_values, key=lambda item: item[1])
    return(max_value_point[1])


# 读取数据
file_path = 'e:/master/dissertation/my-paper/thesis/experiment/data/all.csv'
rate_data = {}
throughput_data = {}

with open(file_path, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        nodes = row['nodes']
        operation = row['operation']
        rate = int(row['rate'])
        throughput = float(row['throughput'])

        if nodes not in rate_data:
            rate_data[nodes] = {}
            throughput_data[nodes] = {}
        if operation not in rate_data[nodes]:
            rate_data[nodes][operation] = []
            throughput_data[nodes][operation] = []
        rate_data[nodes][operation].append(rate)
        throughput_data[nodes][operation].append(throughput)
for nodes, operations in rate_data.items():
    for operation, throughputs in operations.items():
        print(nodes, operation,predict_throughput(rate_data[nodes][operation], throughput_data[nodes][operation]))
