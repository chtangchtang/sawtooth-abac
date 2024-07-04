filename = '../data/PBFT/5node/add_3rate_1'
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
