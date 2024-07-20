import sys
import time
import subprocess
from influxdb import InfluxDBClient


# get arguments
frequency = 1 / int(sys.argv[1])
url = sys.argv[2]

# write start epoch time
client = InfluxDBClient(host='172.21.105.145', port='8086', username='admin', password='admin', database='metrics')
client.write_points([{"measurement": "start_test_check_inquiry", "fields": {'epoch_time': time.time()}}])
client.close()

# start test
for i in range(1000):
    command = "abac check data/inquiry.json --url " + url + " &"
    subprocess.run(command, shell=True)
    time.sleep(frequency)
