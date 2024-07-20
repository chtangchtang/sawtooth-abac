#!/bin/bash
# Stop and remove all containers and volumes
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker volume rm pbft_pbft-shared
docker network rm pbft_default
# Remove and create InfluxDB database
influx -username 'admin' -password 'admin' -execute 'drop database metrics'
influx -username 'admin' -password 'admin' -execute 'create database metrics'
# Start network
nohup docker-compose -f /root/sawtooth-abac/test/pbft/5nodes.yaml up &
# Wait for network to start
sleep 30
# Run tests
docker exec -it abac-client bash -c "cd test && abac add data/policy0.json --url rest-api-0:8008 && sleep 30 && python3 test_check_inquiry_all_rate.py rest-api-0"
# Wait for network to complete consensus
sleep 30
# Export InfluxDB database
influx_inspect export -datadir '/mnt/influxdb/data' -waldir '/mnt/influxdb/wal' -database metrics -out 'output'
# Analyse results
python3 /root/sawtooth-abac/analysis/calculate_time.py output