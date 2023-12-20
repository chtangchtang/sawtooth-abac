import sys
import os
import time


DEFAULT_TXS = 100

send_rate = int(sys.argv[1])
url = sys.argv[2]

for i in range(DEFAULT_TXS):
    os.system("abac add data/policy" + str(i) + ".json --url " + url)
    time.sleep(1 / send_rate)
