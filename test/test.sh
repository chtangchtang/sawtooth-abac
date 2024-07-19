#!/bin/bash
/root/pbft_init.sh
influx -username 'admin' -password 'admin' -execute 'drop database metrics'
influx -username 'admin' -password 'admin' -execute 'create database metrics'
nohub docker-compose -f /root/sawtooth-abac/test/pbft/5nodes.yaml up &
sleep 30
docker exec -it abac-client bash -c "cd test && abac add data/policy0.json --url rest-api--0:8008 && sleep 30 && python3 test_check_inquiry.py 10 rest-api-0:8008"
sleep 30
influx_inspect export -datadir '/mnt/influxdb/data' -waldir '/mnt/influxdb/wal' -database metrics -out 'output'