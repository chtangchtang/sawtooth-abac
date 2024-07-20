import csv
import sys


filename = sys.argv[1]
index = filename.split('/').index('output')
algorithm = filename.split('/')[index+1]
node = int(filename.split('/')[index+2][:-4])
function = filename.split('/')[index+3].split('_')[0]
rate = int(filename.split('/')[index+4].split('_')[1][:-4])
times = int(filename.split('/')[index+5].split('_')[2])

csv_reader = csv.reader(open(filename))
for row in csv_reader:
    if row[0].find('start') > -1:
        start_time = int(row[0].split(' ')[2])
        break

if function == 'check':
    condition = 'count=1001'
else:
    condition = 'count=1000'
csv_reader = csv.reader(open(filename))
flags = [False] * node
end_times = []
for row in csv_reader:
    if row[0] == 'sawtooth_validator.chain.ChainController.committed_transactions_count':
        data = row[1].split(' ')
        for j in range(node):
            if data[0] == 'host=sawtooth-validator-default-' + str(j):
                if data[1] == condition:
                    if not flags[j]:
                        end_times.append(data[2])
                        flags[j] = True
    if False not in flags:
        end_time = int(max(end_times))
        time_usage = (end_time - start_time) / 1000000000
        throughtput = 1000 / time_usage
        break
if False in flags:
    end_time = None
    time_usage = None
    throughtput = None

result = f'{algorithm},{node},{function},{rate},{times},{start_time},{end_time},{time_usage},{throughtput}\n'
print(result)
with open('/root/results.csv', 'a') as f:
    f.write(result)
