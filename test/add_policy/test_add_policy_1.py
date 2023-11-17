import time
import os


for i in range(10000):
    os.system("abac add data/policy" + str(i) + ".json --url 172.18.0.27:8008")
    time.sleep(1)
