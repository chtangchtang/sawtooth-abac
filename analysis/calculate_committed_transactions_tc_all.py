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


output_file = sys.argv[1]
for root, dirs, files in os.walk('/mnt/influxdb/output/pbft'):
    for file in files:
        # 输出文件的完整路径
        filename = os.path.join(root, file)
        committed_transactions_count = find_max_count(filename) - 1
        index = filename.split('/').index('output')
        algorithm = filename.split('/')[index+1]
        node = int(filename.split('/')[index+2][:-4])
        function = filename.split('/')[index+3].split('_')[0]
        rate = int(filename.split('/')[index+3].split('_')[1][:-4])
        result = f'{node},{function},{rate},{committed_transactions_count},\n'
        with open(output_file, 'a') as f:
            f.write(result)
