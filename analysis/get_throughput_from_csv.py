import csv

# 定义CSV文件的路径
csv_file_path = 'results.csv'
count = 0
# 打开CSV文件
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    # 创建一个CSV阅读器
    csvreader = csv.reader(csvfile)
    # 跳过标题行
    next(csvreader)
    # 遍历每一行
    for row in csvreader:
        # 输出每行的最后一个数据
        if row:  # 确保行不为空
            print(row[-1], end=',')
            count += float(row[-1])
print('Total throughput: ', count)
