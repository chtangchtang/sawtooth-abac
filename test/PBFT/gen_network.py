import yaml
import sys
import copy
import json


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
    tmp['entrypoint'] = tmp['entrypoint'].replace('validator-0', 'validator-' + str(i))
    content['services']['abac-tp-python-' + str(i)] = tmp
    # validator
    tmp = copy.deepcopy(content['services']['validator-' + str(i-1)])
    tmp['container_name'] = 'sawtooth-validator-default-' + str(i)
    tmp['hostname'] = 'sawtooth-validator-default-' + str(i)
    tmp['command'] = tmp['command'].replace('validator-' + str(i-1), 'validator-' + str(i))
    tmp['command'] = list(tmp['command'])
    tmp['command'].insert(-3, ' \\\n    --peers tcp://validator-' + str(i-1) + ':8800')
    tmp['command'] = ''.join(tmp['command'])
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
    tmp['entrypoint'] = tmp['entrypoint'].replace('validator-0', 'validator-' + str(i))
    content['services']['settings-tp-' + str(i)] = tmp
    # pbft-engine
    tmp = copy.deepcopy(content['services']['pbft-0'])
    tmp['container_name'] = 'sawtooth-pbft-engine-default-' + str(i)
    tmp['hostname'] = 'sawtooth-pbft-engine-default-' + str(i)
    tmp['entrypoint'] = tmp['entrypoint'].replace('validator-0', 'validator-' + str(i))
    content['services']['pbft-' + str(i)] = tmp

# Write new compose file
f = open(sys.argv[1] + 'nodes.yaml', 'w')
yaml.dump(json.loads(json.dumps(content)), f, Dumper=yaml.SafeDumper)
f.close()