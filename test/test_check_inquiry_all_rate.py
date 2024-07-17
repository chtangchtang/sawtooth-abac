import sys
import subprocess
import time
ip = sys.argv[1]
for i in range(10):
    for j in range(5):
        print('Test rate: ', i * 2 + 3, 'Times: ', j)
        subprocess.run('python3 test_check_inquiry.py '+ str(i * 2 + 3) + ' ' + ip + ':8008', shell=True)
        time.sleep(60)
