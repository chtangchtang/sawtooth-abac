import sys
import os
import time
from influxdb import InfluxDBClient


DEFAULT_TXS = 100

send_rate = int(sys.argv[1])
url = sys.argv[2]

for i in range(DEFAULT_TXS):
    os.system("abac add data/policy" + str(i) + ".json --url " + url)
    time.sleep(1 / send_rate)

print(time.time_ns())
client = InfluxDBClient(host='172.21.105.144', port='8086', username='admin', password='admin', database='metrics')
points = []
points.append({"measurement": "start test add policy", "fields": time.time_ns()})
client.write_points()