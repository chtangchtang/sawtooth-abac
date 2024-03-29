import sys
import os
import time
import socket
from influxdb import InfluxDBClient


DEFAULT_TXS = 1000

send_rate = int(sys.argv[1])
url = sys.argv[2]

# write start epoch time
client = InfluxDBClient(host='172.21.105.145', port='8086', username='admin', password='admin', database='metrics')
points = []
points.append({"measurement": "start_test_add_policy", "fields": {'epoch_time': time.time()}})
client.write_points(points)

# start test
for i in range(DEFAULT_TXS):
    os.system("abac add data/policy" + str(i) + ".json --url " + url + " &")
    time.sleep(1 / send_rate)
