sawtooth-abac

Key commands:
1. influx -username 'admin' -password 'admin'
2. drop database metrics
3. create database metrics
4. influx_inspect export -datadir '/var/lib/influxdb/data/' -waldir '/var/lib/influxdb/wal/' -database metrics -out 'output_file'
5. docker-compose -f sawtooth-abac/test/pbft/5node.yaml up
6. docker inspect rest-api-0 | grep IPAddress
7. docker exec -it abac-client bash
8. cd test/
9. python3 test_xxx.py ip

# docker-tc使用
# cpu和mem数据处理
# 画图
