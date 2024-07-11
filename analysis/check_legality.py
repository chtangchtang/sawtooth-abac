import csv
import sys

filename = sys.argv[1]
with open(filename, newline='') as csvfile:
    reader = csv.reader(csvfile)
    rows = list(reader)

# 遍历每一行，从第二行开始
for i in range(1, len(rows)):
    current = rows[i][5]
    previous = rows[i - 1][6]
    try:
        current = float(current)
        previous = float(previous)
        if current <= previous:
            print('Invalid file!')
            exit()
    except:
        pass
print('Valid file!')