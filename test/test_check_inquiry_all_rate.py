import sys
import subprocess
import time
ip = sys.argv[1]
for i in range(10):
    for j in range(5):
        print('Test rate: ', i, 'Times: ', j)
        if subprocess.run('python3 test_check_inquiry.py '+ str(i * 2 + 3) + ' ' + ip + ':8008', shell=True).returncode:
            sys.exit()
        time.sleep(30)
