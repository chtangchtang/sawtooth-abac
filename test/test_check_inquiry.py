import sys
import os
import time
from influxdb import InfluxDBClient


DEFAULT_TXS = 100

send_rate = int(sys.argv[1])
url = sys.argv[2]

# write start epoch time
client = InfluxDBClient(host='172.21.105.144', port='8086', username='admin', password='admin', database='metrics')
points = []
points.append({"measurement": "start_test_check_inquiry", "fields": {'epoch_time': time.time_ns()}})
client.write_points(points)

# start test
for i in range(DEFAULT_TXS):
    os.system("abac check data/inquiry.json --url " + url)
    time.sleep(1 / send_rate)
