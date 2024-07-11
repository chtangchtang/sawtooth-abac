import csv


data = {}
count = 0
# 定义CSV文件的路径
csv_file_path = 'results.csv'
# 打开CSV文件
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    # 创建一个CSV阅读器
    csvreader = csv.reader(csvfile)
    # 跳过标题行
    next(csvreader)
    # 遍历每一行
    for row in csvreader:
        if int(row[1]) == 7 and row[2] == 'check':
            rate = int(row[3])
            count += float(row[-2])
            try:
                data[rate].append(float(row[-1]))
            except KeyError:
                data[rate] = [float(row[-1])]
# print(data)
print(count)