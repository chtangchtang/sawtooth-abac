import time
import json


start_time = time.time()
for i in range(1000):
    f = open("data/inquiry.json", "r")
    f = f.read()
    data = json.loads(f)
    # print(data)
end_time = time.time()
print("Time taken:", end_time - start_time)