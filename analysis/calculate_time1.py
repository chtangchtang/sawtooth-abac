import csv
import sys


filename = sys.argv[1]
flags = [False, False, False, False, False]
times = []
csv_reader = csv.reader(open(filename))
count = 1001
condition = 'count=' + str(count)
for row in csv_reader:
    try:
        if row[0].find('start_test_check_inquiry') > -1:
            data = row[0].split(' ')
            start_time = data[2]
            print(start_time, end=',')
            flags = [False, False, False, False, False]
        if row[0] == 'sawtooth_validator.chain.ChainController.committed_transactions_count':
            data = row[1].split(' ')
            if data[0] == 'host=sawtooth-validator-default-0':
                if data[1] == condition:
                    if not flags[0]:
                        times.append(data[2])
                        flags[0] = True
            if data[0] == 'host=sawtooth-validator-default-1':
                if data[1] == condition:
                    if not flags[1]:
                        times.append(data[2])
                        flags[1] = True
            if data[0] == 'host=sawtooth-validator-default-2':
                if data[1] == condition:
                    if not flags[2]:
                        times.append(data[2])
                        flags[2] = True
            if data[0] == 'host=sawtooth-validator-default-3':
                if data[1] == condition:
                    if not flags[3]:
                        times.append(data[2])
                        flags[3] = True
            if data[0] == 'host=sawtooth-validator-default-4':
                 if data[1] == condition:
                     if not flags[4]:
                         times.append(data[2])
                         flags[4] = True
        if flags[0] and flags[1] and flags[2] and flags[3] and flags[4]:
           end_time = max(times)
           print(end_time, end=',')
           time_usage = (int(end_time) - int(start_time)) / 1000000000
           print(time_usage, end=',')
           print(1000 / time_usage)
           count += 1000
           condition = 'count=' + str(count)
    finally:
        pass
