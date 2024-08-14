import csv
import sys


filename = sys.argv[1]
output_file = sys.argv[2]
index = filename.split('/').index('output')
algorithm = filename.split('/')[index+1]
node = int(filename.split('/')[index+2][:-4])
function = filename.split('/')[index+3].split('_')[0]
rate = int(filename.split('/')[index+3].split('_')[1][:-4])
times = int(filename.split('/')[index+3].split('_')[2])

start_times = []
csv_reader = csv.reader(open(filename))
for row in csv_reader:
    if row[0].find('start') > -1:
        start_times.append(int(row[0].split(' ')[2]))
        if len(start_times) == 2:
            break
start_times.sort()

# Calculate time for add
csv_reader = csv.reader(open(filename))
flags = [False] * node
end_times = []
for row in csv_reader:
    if row[0] == 'sawtooth_validator.chain.ChainController.committed_transactions_count':
        data = row[1].split(' ')
        for j in range(node):
            if data[0] == 'host=sawtooth-validator-default-' + str(j):
                if data[1] == 'count=1000':
                    if not flags[j]:
                        end_times.append(data[2])
                        flags[j] = True
    if False not in flags:
        end_time = int(max(end_times))
        time_usage = (end_time - start_times[0]) / 1000000000
        throughtput = 1000 / time_usage
        break
if False in flags:
    end_time = None
    time_usage = None
    throughtput = None

result = f'{algorithm},{node},{"add"},{rate},{times},{start_times[0]},{end_time},{time_usage},{throughtput}\n'
with open(output_file, 'a') as f:
    f.write(result)

# Calculate time for delete
csv_reader = csv.reader(open(filename))
flags = [False] * node
end_times = []
for row in csv_reader:
    if row[0] == 'sawtooth_validator.chain.ChainController.committed_transactions_count':
        data = row[1].split(' ')
        for j in range(node):
            if data[0] == 'host=sawtooth-validator-default-' + str(j):
                if data[1] == 'count=2000':
                    if not flags[j]:
                        end_times.append(data[2])
                        flags[j] = True
    if False not in flags:
        end_time = int(max(end_times))
        time_usage = (end_time - start_times[1]) / 1000000000
        throughtput = 1000 / time_usage
        break
if False in flags:
    end_time = None
    time_usage = None
    throughtput = None

result = f'{algorithm},{node},{"delete"},{rate},{times},{start_times[1]},{end_time},{time_usage},{throughtput}\n'
with open(output_file, 'a') as f:
    f.write(result)
