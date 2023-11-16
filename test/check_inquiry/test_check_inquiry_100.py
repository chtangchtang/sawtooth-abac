import time
import os


while True:
    os.system("abac check inquiry.json --url 172.18.0.27:8008")
    time.sleep(0.01)
