#!/bin/bash

for rate in 3 5 7 9 11 13 15
do
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

    # Run test
    # Add policy for testing check inquiry
    docker exec -it abac-client bash -c "cd test && abac add data/policy0.json --url rest-api-0:8008"
    # Wait for network to complete consensus
    sleep 30
    # Test check inquiry
    docker exec -it abac-client bash -c "python3 test_check_inquiry.py 10 rest-api-0:8008"
    # Wait for network to complete consensus
    sleep 30

    # Export InfluxDB database
    influx_inspect export -datadir '/mnt/influxdb/data' -waldir '/mnt/influxdb/wal' -database metrics -out '/root/data/pbft/5node/'
    # Analyse results
    python3 /root/sawtooth-abac/analysis/calculate_time.py output
done
