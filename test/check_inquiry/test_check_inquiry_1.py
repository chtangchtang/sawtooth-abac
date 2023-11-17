import time
import os
import json


inquiry = {
    "subject": {
        "id": "",
        "attributes": {
            "name": "Max"
        }
    },
    "resource": {
        "id": "",
        "attributes": {
            "name": "myrn:example.com:resource:123"
        }
    },
    "action": {
        "id": "",
        "attributes": {
            "method": "get"
        }
    },
    "context": {
        "ip": "127.0.0.1"
    }
}

with open('inquiry.json', 'w') as f:
    json.dump(inquiry, f)

while True:
    os.system("abac check inquiry.json --url 172.18.0.27:8008")
    time.sleep(1)
