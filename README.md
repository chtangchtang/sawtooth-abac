sawtooth-abac

Key commands:
1. influx -username 'admin' -password 'admin'
2. influx_inspect export -datadir '/var/lib/influxdb/data/' -waldir '/var/lib/influxdb/wal/' -database metrics -out ''
3. docker-compose -f sawtooth-abac/test/pbft/5node.yaml up
4. docker inspect rest-api-0 | grep IPAddress
5. docker exec -it abac-client bash
6. cd test/
7. python3 test_xxx.py ip
