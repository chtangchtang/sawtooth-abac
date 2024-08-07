#!/bin/bash

for rate in 21 19 17 15 13 11 9 7 5 3 
do
    for times in {0..6}
    do
        ## Down network
        docker-compose -f /root/sawtooth-abac/test/pbft/5nodes.yaml down -v

        # Remove and create InfluxDB database
        influx -username 'admin' -password 'admin' -execute 'drop database metrics'
        influx -username 'admin' -password 'admin' -execute 'create database metrics'

        # Up network
        docker-compose -f /root/sawtooth-abac/test/pbft/5nodes.yaml up &
        # Wait for network to start
        sleep 60

        # Add a policy for testing check inquiry and test check inquiry
        docker exec -it abac-client bash -c "cd test && abac add data/policy0.json --url rest-api-0:8008 && sleep 60 && python3 test_check_inquiry.py $rate rest-api-0:8008 && sleep 60"

        # Export InfluxDB database
        influx_inspect export -datadir '/mnt/influxdb/data' -waldir '/mnt/influxdb/wal' -database metrics -out "/mnt/influxdb/output/pbft/5node/check_${rate}rate_${times}"
        # Analyse results
        python3 /root/sawtooth-abac/analysis/calculate_time.py /mnt/influxdb/output/pbft/5node/check_${rate}rate_${times} /root/pbft_5node_check_result.csv

        # Down network
        docker-compose -f /root/sawtooth-abac/test/pbft/5nodes.yaml down -v
    done
done
