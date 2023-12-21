import json
import os
import sys


policy = {
    "uid": "0",
    "description": "Users with level not less than 5 can only use administrator applications to delete or add the flow between 8 AM and 5 PM.",
    "effect": "allow",
    "rules": {
        "subject": [
            {
                "$.user-level": {
                    "condition": "Gte",
                    "value": 5
                }
            },
            {
                "$.type": {
                    "condition": "Equals",
                    "value": "admin"
                }
            }
        ],
        "resource": {
            "$.type": {
                "condition": "Equals",
                "value": "flow"
            }
        },
        "action": [
            {
                "$.method": {
                    "condition": "Equals",
                    "value": "add"
                }
            },
            {
                "$.method": {
                    "condition": "Equals",
                    "value": "delete"
                }
            }
        ],
        "context": {
            "$.time": {
                "condition": "Gte",
                "value": 8
            },
            "$.time": {
                "condition": "Lte",
                "value": 17
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
