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
        if row[0].find('start') > -1:
            data = row[0].split(' ')
            start_time = data[2]
            print(start_time, end=',')
    finally:
        pass
