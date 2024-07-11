import sys


input_file = sys.argv[1]  # 输入文件路径
output_file = input_file + '.extracted'  # 输出文件路径
keywords = ['start', 'committed_transactions_count', 'cpu', 'mem']  # 关键字列表
try:
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            if any(keyword in line for keyword in keywords):
                outfile.write(line)
    print(f"Extracted data saved to {output_file}")
except Exception as e:
    print(f"Exception occurred: {e}")
