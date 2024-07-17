import sys
import time
import subprocess
from influxdb import InfluxDBClient


send_rate = int(sys.argv[1])
url = sys.argv[2]
policy_range = range(int(sys.argv[3]), int(sys.argv[3]) + 1000)

# write start epoch time
client = InfluxDBClient(host='172.21.105.145', port='8086', username='admin', password='admin', database='metrics')
client.write_points([{"measurement": "start_test_delete_policy", "fields": {'epoch_time': time.time()}}])
client.close()

# start test
for i in policy_range:
    command = "abac delete data/policy" + str(i) + ".json --url " + url + " &"
    subprocess.run(command, shell=True)
    time.sleep(1 / send_rate)
