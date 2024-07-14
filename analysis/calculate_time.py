import csv
import sys
import time

round = 50

start_time = []
end_time = []
time_usage = []
throughtput = []

filename = sys.argv[1]
index = filename.split('/').index('data')
algorithm = filename.split('/')[index+1]
node = int(filename.split('/')[index+2][:-4])
function = filename.split('/')[index+3]

csv_reader = csv.reader(open(filename))
for row in csv_reader:
    if row[0].find('start') > -1:
        start_time.append(int(row[0].split(' ')[2]))
        if len(start_time) == round:
            break
start_time.sort()

for i in range(round):
    if function == 'check':
        flag = 'count=' + str(i + 1) + '001'
    else:
        flag = 'count=' + str(i + 1) + '000'
    csv_reader = csv.reader(open(filename))
    flags = [False] * node
    times = []
    for row in csv_reader:
        if row[0] == 'sawtooth_validator.chain.ChainController.committed_transactions_count':
            data = row[1].split(' ')
            for j in range(node):
                if data[0] == 'host=sawtooth-validator-default-' + str(j):
                    if data[1] == flag:
                        if not flags[j]:
                            times.append(data[2])
                            flags[j] = True
        if False not in flags:
            end_time.append(int(max(times)))
            time_usage.append((end_time[i] - start_time[i]) / 1000000000)
            throughtput.append(1000 / time_usage[i])
            rate = (i // 5 + 1) * 2 + 1
            times = i % 5
            result = f'{algorithm},{node},{function},{rate},{times},{start_time[i]},{end_time[i]},{time_usage[i]},{throughtput[i]}\n'
            print(result)
            with open('/root/results.csv', 'a') as f:
                f.write(result)
            break
    if False in flags:
        raise RuntimeError('Round ' + str(i) + ' Cannot find end time for all nodes')
