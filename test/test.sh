#!/bin/bash

for rate in 3 5 7 9 11 13 15 17 19 21
do
    for times in 0 1 2 3 4 5 6
    do
        # Stop and remove all containers and volumes
        docker stop $(docker ps -a -q) > /dev/null
        docker rm $(docker ps -a -q) > /dev/null
        docker volume rm pbft_pbft-shared > /dev/null
        docker network rm pbft_default > /dev/null

        # Remove and create InfluxDB database
        influx -username 'admin' -password 'admin' -execute 'drop database metrics'
        influx -username 'admin' -password 'admin' -execute 'create database metrics'

        # Start network
        nohup docker-compose -f /root/sawtooth-abac/test/pbft/5nodes.yaml up > /dev/null 2>&1 &
        # Wait for network to start
        sleep 30

        # Run test
        # Add a policy for testing check inquiry
        docker exec -it abac-client bash -c "cd test && abac add data/policy0.json --url rest-api-0:8008"
        # Wait for network to complete consensus
        sleep 30
        # Test check inquiry
        docker exec -it abac-client bash -c "cd test && python3 test_check_inquiry.py $rate rest-api-0:8008"
        # Wait for network to complete consensus
        sleep 60

        # Export InfluxDB database
        influx_inspect export -datadir '/mnt/influxdb/data' -waldir '/mnt/influxdb/wal' -database metrics -out "/mnt/influxdb/output/pbft/5node/check_${rate}rate_${times}"
        # Analyse results
        python3 /root/sawtooth-abac/analysis/calculate_time.py /mnt/influxdb/output/pbft/5node/check_${rate}rate_${times}
    done
done
