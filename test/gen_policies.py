import json
import os
import sys


policy = {
    "uid": "0",
    "description": "Max and Nina are allowed to create, delete, get any resources only if the client IP matches.",
    "effect": "allow",
    "rules": {
        "subject": [
            {
                "$.name": {
                    "condition": "Equals",
                    "value": "Max"
                }
            },
            {
                "$.name": {
                    "condition": "Equals",
                    "value": "Nina"
                }
            }
        ],
        "resource": {
            "$.name": {
                "condition": "RegexMatch",
                "value": ".*"
            }
        },
        "action": [
            {
                "$.method": {
                    "condition": "Equals",
                    "value": "create"
                }
            },
            {
                "$.method": {
                    "condition": "Equals",
                    "value": "delete"
                }
            },
            {
                "$.method": {
                    "condition": "Equals",
                    "value": "get"
                }
            }
        ],
        "context": {
            "$.ip": {
                "condition": "CIDR",
                "value": "127.0.0.1/32"
            }
        }
    },
    "targets": {},
    "priority": 0
}

try:
    os.mkdir('data')
except:
    pass
for i in range(int(sys.argv[1])):
    with open('data/policy' + str(i) + '.json', 'w') as f:
        policy["uid"] = str(i)
        json.dump(policy, f)
print("Generated " + sys.argv[1] + " policies.")
