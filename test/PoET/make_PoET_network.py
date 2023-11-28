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
    tmp['command'] = tmp['command'].replace('validator-0', 'validator-' + str(i))
    content['services']['abac-tp-python-' + str(i)] = tmp
    # validator
    tmp = copy.deepcopy(content['services']['validator-' + str(i-1)])
    tmp['container_name'] = 'sawtooth-validator-default-' + str(i)
    tmp['hostname'] = 'sawtooth-validator-default-' + str(i)
    tmp['command'] = tmp['command'].replace('validator-' + str(i-1), 'validator-' + str(i))
    index = tmp['command'].find('validator-' + str(i - 2))
    tmp['command'] = list(tmp['command'])
    tmp['command'].insert(index + 16, ',tcp://validator-' + str(i-1) + ':8800')
    tmp['command'] = ''.join(tmp['command'])
    content['services']['validator-' + str(i)] = tmp
    # rest-api
    tmp = copy.deepcopy(content['services']['rest-api-0'])
    tmp['container_name'] = 'rest-api-' + str(i)
    tmp['hostname'] = 'rest-api-' + str(i)
    tmp['command'] = tmp['command'].replace('validator-0', 'validator-' + str(i))
    tmp['command'] = tmp['command'].replace('rest-api-0', 'rest-api-' + str(i))
    content['services']['rest-api-' + str(i)] = tmp
    # settings-tp
    tmp = copy.deepcopy(content['services']['settings-tp-0'])
    tmp['container_name'] = 'settings-tp-' + str(i)
    tmp['hostname'] = 'settings-tp-' + str(i)
    tmp['command'] = tmp['command'].replace('validator-0', 'validator-' + str(i))
    content['services']['settings-tp-' + str(i)] = tmp
    # poet-engine
    tmp = copy.deepcopy(content['services']['poet-engine-0'])
    tmp['container_name'] = 'poet-engine-' + str(i)
    tmp['hostname'] = 'poet-engine-' + str(i)
    tmp['command'] = tmp['command'].replace('validator-0', 'validator-' + str(i))
    content['services']['poet-engine-' + str(i)] = tmp
    # poet-validator-registry-tp
    tmp = copy.deepcopy(content['services']['poet-validator-registry-tp-0'])
    tmp['container_name'] = 'poet-validator-registry-tp-' + str(i)
    tmp['hostname'] = 'poet-validator-registry-tp-' + str(i)
    tmp['command'] = tmp['command'].replace('validator-0', 'validator-' + str(i))
    content['services']['poet-validator-registry-tp-' + str(i)] = tmp

# Write new compose file
f = open(sys.argv[1] + 'nodes.yaml', 'w')
yaml.dump(json.loads(json.dumps(content)), f, Dumper=yaml.Dumper)
f.close()
