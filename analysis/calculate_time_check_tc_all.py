import csv
import sys
import re
import os


# 定义一个函数来找出最大 count 值
def find_max_count(file_path):
    max_count = None
    # 使用正则表达式匹配包含 'committed_transactions_count' 的行中的 count 值
    pattern = r'committed_transactions_count.*count=(\d+)'
    # 读取文件
    with open(file_path, 'r') as file:
        for line in file:
            match = re.search(pattern, line)
            if match:
                count_value = int(match.group(1))
                if max_count is None or count_value > max_count:
                    max_count = count_value   
    return max_count


for root, dirs, files in os.walk('/mnt/influxdb/output/pbft'):
    for file in files:
        # 输出文件的完整路径
        filename = os.path.join(root, file)
        max_count_value = find_max_count(filename)

        output_file = sys.argv[1]
        index = filename.split('/').index('output')
        algorithm = filename.split('/')[index+1]
        node = int(filename.split('/')[index+2][:-4])
        function = filename.split('/')[index+3].split('_')[0]
        rate = int(filename.split('/')[index+3].split('_')[1][:-4])
        times = filename.split('/')[index+3].split('_')[2]

        csv_reader = csv.reader(open(filename))
        for row in csv_reader:
            if row[0].find('start') > -1:
                start_time = int(row[0].split(' ')[2])
                break

        csv_reader = csv.reader(open(filename))
        flags = [False] * node
        end_times = []
        for row in csv_reader:
            if row[0] == 'sawtooth_validator.chain.ChainController.committed_transactions_count':
                data = row[1].split(' ')
                for j in range(node):
                    if data[0] == 'host=sawtooth-validator-default-' + str(j):
                        if data[1] == 'count=' + str(max_count_value):
                            if not flags[j]:
                                end_times.append(data[2])
                                flags[j] = True
            if False not in flags:
                end_time = int(max(end_times))
                time_usage = (end_time - start_time) / 1000000000
                throughtput = (max_count_value - 1) / time_usage
                break
        if False in flags:
            end_time = None
            time_usage = None
            throughtput = None

        result = f'{algorithm},{node},{function},{rate},{times},{start_time},{end_time},{time_usage},{throughtput}\n'
        with open(output_file, 'a') as f:
            f.write(result)
