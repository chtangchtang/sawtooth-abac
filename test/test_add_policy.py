import sys
import time
import subprocess
from influxdb import InfluxDBClient


send_rate = int(sys.argv[1])
url = sys.argv[2]
policy_range = range(int(sys.argv[3]), int(sys.argv[3]) + 1000)
# write start epoch time
client = InfluxDBClient(host='172.21.105.145', port='8086', username='admin', password='admin', database='metrics')
points = []
points.append({"measurement": "start_test_add_policy", "fields": {'epoch_time': time.time()}})
client.write_points(points)

# start test
for i in policy_range:
    command = "abac add data/policy" + str(i) + ".json --url " + url + " &"
    subprocess.run(command, shell=True)
    time.sleep(1 / send_rate)
