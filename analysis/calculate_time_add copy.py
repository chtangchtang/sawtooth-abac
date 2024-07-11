import csv
import sys

start_time = []
filename = sys.argv[1]
csv_reader = csv.reader(open(filename))
for row in csv_reader:
    if row[0].find('start') > -1:
        start_time.append(int(row[0].split(' ')[2]))
        # print(start_time, end=',')
        if len(start_time) == 50:
            break
start_time.sort()

end_time = []
for i in range(50):
    flag = 'count=' + str(i + 1) + '000'
    csv_reader = csv.reader(open(filename))
    flags = [False, False, False, False, False]
    times = []
    for row in csv_reader:
        if row[0] == 'sawtooth_validator.chain.ChainController.committed_transactions_count':
            data = row[1].split(' ')
            if data[0] == 'host=sawtooth-validator-default-0':
                if data[1] == flag:
                    if not flags[0]:
                        times.append(data[2])
                        flags[0] = True
            if data[0] == 'host=sawtooth-validator-default-1':
                if data[1] == flag:
                    if not flags[1]:
                        times.append(data[2])
                        flags[1] = True
            if data[0] == 'host=sawtooth-validator-default-2':
                if data[1] == flag:
                    if not flags[2]:
                        times.append(data[2])
                        flags[2] = True
            if data[0] == 'host=sawtooth-validator-default-3':
                if data[1] == flag:
                    if not flags[3]:
                        times.append(data[2])
                        flags[3] = True
            if data[0] == 'host=sawtooth-validator-default-4':
                    if data[1] == flag:
                        if not flags[4]:
                            times.append(data[2])
                            flags[4] = True
        if flags[0] and flags[1] and flags[2] and flags[3] and flags[4]:
            end_time.append(int(max(times)))
            # print(end_time, end=',')
            break
end_time.sort()

time_usage = [0] * 50
throughtput = [0] * 50
for i in range(50):
    time_usage[i] = (end_time[i] - start_time[i]) / 1000000000
    throughtput[i] = 1000 / time_usage[i]
# print(time_usage, end=',')
# print(1000 / time_usage)

index = filename.split('/').index('data')
algorithm = filename[index+1]
node = int(filename[index+2][:-4])
function = 'check'
with open('/root/results.csv', 'a') as f:
    for i in range(50):
        rate = (i // 5 + 1) * 2 + 1
        times = i % 5
        f.write(f'{algorithm},{node},{function},{rate},{times},{start_time[i]},{end_time[i]},{time_usage[i]},{throughtput[i]}\n')
        print(f'{algorithm},{node},{function},{rate},{times},{start_time[i]},{end_time[i]},{time_usage[i]},{throughtput[i]}')
