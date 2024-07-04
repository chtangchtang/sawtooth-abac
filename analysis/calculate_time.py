import csv
import sys


filename = sys.argv[1]
csv_reader = csv.reader(open(filename))
for row in csv_reader:
    if row[0].find('start') > -1:
        start_time = row[0].split(' ')[2]
        print(start_time, end=',')
        break

csv_reader = csv.reader(open(filename))
flags = [False, False, False, False, False]
times = []
for row in csv_reader:
    if row[0] == 'sawtooth_validator.chain.ChainController.committed_transactions_count':
        data = row[1].split(' ')
        if data[0] == 'host=sawtooth-validator-default-0':
            if data[1] == 'count=1000':
                if not flags[0]:
                    times.append(data[2])
                    flags[0] = True
        if data[0] == 'host=sawtooth-validator-default-1':
            if data[1] == 'count=1000':
                if not flags[1]:
                    times.append(data[2])
                    flags[1] = True
        if data[0] == 'host=sawtooth-validator-default-2':
            if data[1] == 'count=1000':
                if not flags[2]:
                    times.append(data[2])
                    flags[2] = True
        if data[0] == 'host=sawtooth-validator-default-3':
            if data[1] == 'count=1000':
                if not flags[3]:
                    times.append(data[2])
                    flags[3] = True
        if data[0] == 'host=sawtooth-validator-default-4':
                if data[1] == 'count=1000':
                    if not flags[4]:
                        times.append(data[2])
                        flags[4] = True
    if flags[0] and flags[1] and flags[2] and flags[3] and flags[4]:
        end_time = max(times)
        print(end_time, end=',')
        break

time_usage = (int(end_time) - int(start_time)) / 1000000000
print(time_usage, end=',')
print(1000 / time_usage)

filename = filename.split('/')
for i in range(len(filename)):
    if filename[i] == 'data':
        algorithm = filename[i+1]
        node = int(filename[i+2][0])
        s = filename[i+3].split('_')
        function = s[0]
        rate = int(s[1][0])
        times = int(s[2])
        print(algorithm, node, function, rate, times, end=',')
        break
with open('/root/results.csv', 'a') as f:
    f.write(f'{algorithm},{node},{function},{rate},{times},{start_time},{end_time},{time_usage},{1000/time_usage}\n')