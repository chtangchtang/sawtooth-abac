#!/bin/bash


for rate in 15 13 11 9 7 5 3 1
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
        docker-compose -f /root/sawtooth-abac/test/pbft/13nodes.yaml up &
        # Wait for network to start
        sleep 60
        # Test add and delete policy
        docker exec -it abac-client bash -c "cd test && python3 test_add_policy.py $rate rest-api-0:8008 && sleep 600 && python3 test_delete_policy.py $rate rest-api-0:8008 && sleep 600"
        # Export InfluxDB database
        influx_inspect export -datadir '/mnt/influxdb/data' -waldir '/mnt/influxdb/wal' -database metrics -out "/mnt/influxdb/output/pbft/13node/add+delete_${rate}rate_${times}"
        # Analyse results
        python3 /root/sawtooth-abac/analysis/calculate_time_add+delete.py /mnt/influxdb/output/pbft/13node/add+delete_${rate}rate_${times} /root/pbft_13node_result.csv
        # Down network
        docker-compose -f /root/sawtooth-abac/test/pbft/13nodes.yaml down -v
    done
done
# Compress result files and remove them
tar -czvf /mnt/influxdb/output/pbft_13node_add+delete.tar.gz /mnt/influxdb/output/pbft/13node/
rm /mnt/influxdb/output/pbft/13node/*
