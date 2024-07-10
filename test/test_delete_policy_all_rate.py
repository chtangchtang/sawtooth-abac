import sys
import subprocess
import time
ip = sys.argv[1]
for i in range(10):
    for j in range(5):
        subprocess.run('python3 test_delete_policy.py '+ str(i * 2 + 3) + ' ' + ip + ':8008' +' ' + str((i * 5 + j) * 1000), shell=True)
        time.sleep(30)
