#!/bin/bash

for rate in 21 19 17 15 13 11 9 7 5 3 
do
    for times in 0 1 2 3 4 5 6
    do
        # Stop and remove all containers and volumes
        running_containers=$(docker ps -q)
        if [ -n "$running_containers" ]; then
            docker stop $running_containers > /dev/null
        fi
        all_containers=$(docker ps -a -q)
        if [ -n "$all_containers" ]; then
            docker rm $all_containers > /dev/null
        fi
        all_volumes=$(docker volume ls -q)
        if [ -n "$all_volumes" ]; then
            docker volume rm $all_volumes > /dev/null
        fi
        all_networks=$(docker network ls -q)
        if [ -n "$all_networks" ]; then
            docker network rm $all_networks > /dev/null
        fi

        # Remove and create InfluxDB database
        influx -username 'admin' -password 'admin' -execute 'drop database metrics'
        influx -username 'admin' -password 'admin' -execute 'create database metrics'

        # Start network
        docker-compose -f /root/sawtooth-abac/test/pbft/5nodes.yaml up > /dev/null 2>&1 &
        # Wait for network to start
        sleep 30

        # Run test
        # Add a policy for testing check inquiry
        docker exec -it abac-client bash -c "cd test && abac add data/policy0.json --url rest-api-0:8008 && sleep 60"
        # Test check inquiry
        docker exec -it abac-client bash -c "cd test && python3 test_check_inquiry.py $rate rest-api-0:8008 && sleep 60"

        # Export InfluxDB database
        influx_inspect export -datadir '/mnt/influxdb/data' -waldir '/mnt/influxdb/wal' -database metrics -out "/mnt/influxdb/output/pbft/5node/check_${rate}rate_${times}" > /dev/null
        # Analyse results
        python3 /root/sawtooth-abac/analysis/calculate_time.py /mnt/influxdb/output/pbft/5node/check_${rate}rate_${times} /root/pbft_5node_check_result.csv

        # Stop and remove all containers and volumes
        docker stop $(docker ps -q) > /dev/null
        docker rm $(docker ps -a -q) > /dev/null
        docker volume rm $(docker volume ls -q) > /dev/null
        docker network rm $(docker network ls -q) > /dev/null
    done
done
