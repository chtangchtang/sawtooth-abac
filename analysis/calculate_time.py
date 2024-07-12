import csv
import sys
import time

s = time.time()

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
        if len(start_time) == 50:
            break
start_time.sort()

for i in range(50):
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
            break
end_time.sort()

with open('/root/results.csv', 'a') as f:
    for i in range(50):
        rate = (i // 5 + 1) * 2 + 1
        times = i % 5
        time_usage.append((end_time[i] - start_time[i]) / 1000000000)
        throughtput.append(1000 / time_usage[i])
        result = f'{algorithm},{node},{function},{rate},{times},{start_time[i]},{end_time[i]},{time_usage[i]},{throughtput[i]}\n'
        # f.write(result)
        print(result)

e = time.time()
print('Runtime: ', e-s)