#!/bin/bash


for rate in 9 7 5 3 1
do
    for times in 0
    do
        ## Clean up network
        docker stop $(docker ps -a -q)
        docker rm $(docker ps -a -q)
        docker network rm $(docker network ls -q)
        docker volume rm $(docker volume ls -q)
        # Remove and create InfluxDB database
        influx -username 'admin' -password 'admin' -execute 'drop database metrics'
        influx -username 'admin' -password 'admin' -execute 'create database metrics'

        # Up network
        docker-compose -f /root/sawtooth-abac/test/pbft/11nodes.yaml up &
        # Wait for network to start
        sleep 60
        # Add a policy for testing check inquiry and test check inquiry
        docker exec -it abac-client bash -c "cd test && abac add data/policy0.json --url rest-api-0:8008 && sleep 300 && python3 test_check_inquiry.py $rate rest-api-0:8008 && sleep 300"
        # Export InfluxDB database
        influx_inspect export -datadir '/mnt/influxdb/data' -waldir '/mnt/influxdb/wal' -database metrics -out "/mnt/influxdb/output/pbft/11node/check_${rate}rate_${times}"
        # Analyse results
        python3 /root/sawtooth-abac/analysis/calculate_time_check.py /mnt/influxdb/output/pbft/11node/check_${rate}rate_${times} /root/pbft_11node_result.csv
        # Down network
        docker-compose -f /root/sawtooth-abac/test/pbft/11nodes.yaml down -v
    done
done
# Compress result files and remove them
tar -czvf /mnt/influxdb/output/pbft_11node_check.tar.gz /mnt/influxdb/output/pbft/11node/
rm /mnt/influxdb/output/pbft/11node/*
