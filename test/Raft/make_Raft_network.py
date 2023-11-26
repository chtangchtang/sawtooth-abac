import yaml
import sys
import copy
import json


def get_other_peers(nums, my_num):
    all_peers = ''
    for i in range(nums):
        if i != my_num:
            all_peers += 'tcp://validator-' + str(i) + ':8800,'
    return all_peers[:-1]

# Read basic compose file
f = open('5nodes.yaml', 'r')
content = yaml.load(f.read(), Loader=yaml.FullLoader)
f.close()

# Add services
new_num = int(sys.argv[1])
old_num = int(list(content['services'].keys())[-1][-1]) + 1

for i in range(old_num, new_num):
    # abac-tp
    tmp = copy.deepcopy(content['services']['abac-tp-python-0'])
    tmp['container_name'] = 'abac-tp-python-default-' + str(i)
    tmp['hostname'] = 'abac-tp-python-default-' + str(i)
    tmp['command'] = tmp['command'].replace('validator-0', 'validator-' + str(i))
    content['services']['abac-tp-python-' + str(i)] = tmp
    # validator
    tmp = copy.deepcopy(content['services']['validator-1'])
    tmp['container_name'] = 'sawtooth-validator-default-' + str(i)
    tmp['hostname'] = 'sawtooth-validator-default-' + str(i)
    tmp['command'] = tmp['command'].replace('validator-1', 'validator-' + str(i))
    index = tmp['command'].find('--peers')
    s1 = tmp['command'][:index+8]
    s3 = tmp['command'][index+99:]
    s2 = get_other_peers(new_num, i)
    tmp['command'] = s1 + s2 + s3
    content['services']['validator-' + str(i)] = tmp
    # rest-api
    tmp = copy.deepcopy(content['services']['rest-api-0'])
    tmp['container_name'] = 'rest-api-' + str(i)
    tmp['hostname'] = 'rest-api-' + str(i)
    tmp['ports'][0] = '800' + str(i) + ':8008'
    tmp['depends_on'][0] = tmp['depends_on'][0].replace('0', str(i))
    tmp['command'] = tmp['command'].replace('validator-0', 'validator-' + str(i))
    tmp['command'] = tmp['command'].replace('rest-api-0', 'rest-api-' + str(i))
    content['services']['rest-api-' + str(i)] = tmp
    # settings-tp
    tmp = copy.deepcopy(content['services']['settings-tp-0'])
    tmp['container_name'] = 'settings-tp-' + str(i)
    tmp['hostname'] = 'settings-tp-' + str(i)
    tmp['depends_on'][0] = tmp['depends_on'][0].replace('0', str(i))
    tmp['command'] = tmp['command'].replace('validator-0', 'validator-' + str(i))
    content['services']['settings-tp-' + str(i)] = tmp
    # raft-engine
    tmp = copy.deepcopy(content['services']['raft-0'])
    tmp['container_name'] = 'sawtooth-raft-engine-default-' + str(i)
    tmp['hostname'] = 'sawtooth-raft-engine-default-' + str(i)
    tmp['command'] = tmp['command'].replace('validator-0', 'validator-' + str(i))
    content['services']['raft-' + str(i)] = tmp

# validator-0
index = content['services']['validator-0']['command'].find('sawadm keygen &&')
content['services']['validator-0']['command'] = list(content['services']['validator-0']['command'])
data = ''
for i in range(old_num, new_num):
    data += "sawadm keygen validator-" + str(i) + " && \\\n  "
content['services']['validator-0']['command'].insert(index, data)
content['services']['validator-0']['command'] = ''.join(content['services']['validator-0']['command'])
index = content['services']['validator-0']['command'].find('--peers')
s1 = content['services']['validator-0']['command'][:index+8]
s3 = content['services']['validator-0']['command'][index+99:]
s2 = get_other_peers(new_num, 0)
content['services']['validator-0']['command'] = s1 + s2 + s3
index = content['services']['validator-0']['command'].find('cat /etc/sawtooth/keys/validator-4.pub')
data = ''
for i in range(old_num, new_num):
    s1 = r",'\"'$$(cat /etc/sawtooth/keys/validator-4.pub)'"
    s2 = r"\"'"
    s = s1 + s2
    s = s.replace('4', str(i))
    data += s
content['services']['validator-0']['command'] = list(content['services']['validator-0']['command'])
content['services']['validator-0']['command'].insert(index + 43, data)
content['services']['validator-0']['command'] = ''.join(content['services']['validator-0']['command'])

# Write new compose file
f = open(sys.argv[1] + 'nodes.yaml', 'w')
yaml.dump(json.loads(json.dumps(content)), f, Dumper=yaml.Dumper)
f.close()
