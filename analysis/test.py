import csv


f = open('output', 'w')
csv_reader = csv.reader(open("pbft/pbft_5node_100rate_100policy"))
for row in csv_reader:
    try:
        if row[0] == 'sawtooth_validator.chain.ChainController.committed_transactions_count':
            # if row[1][:33] == 'host=sawtooth-validator-default-4':
                # print(row)
            f.write(str(row))
            f.write('\n')
    finally:
        continue
