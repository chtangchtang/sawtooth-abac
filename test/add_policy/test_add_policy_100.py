import time
import os
import json


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

# Generate 10000 policies.
for i in range(10000):
    with open('policy' + str(i) + '.json', 'w') as f:
        policy["uid"] = str(i)
        json.dump(policy, f)
print("Generated 10000 policies.")

for i in range(10000):
    os.system("abac add policy" + str(i) + ".json --url 172.18.0.27:8008")
    time.sleep(0.01)
