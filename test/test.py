import os
import time

s = time.time()
rate = 10
for i in range(100):
    os.system("ls &")
    # time.sleep(1/rate)

e = time.time()

print(e-s)

