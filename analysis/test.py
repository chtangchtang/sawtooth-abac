filename = 'data/pbft/51node/add_11rate_0'
filename = filename.split('/')
for i in range(len(filename)):
    if filename[i] == 'data':
        algorithm = filename[i+1]
        node = int(filename[i+2][:-4])
        s = filename[i+3].split('_')
        function = s[0]
        rate = int(s[1][:-4])
        times = int(s[2])
        break
print(f'{algorithm},{node},{function},{rate},{times}')