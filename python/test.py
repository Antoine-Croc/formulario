import sys
import json
from pathlib import *
import pathlib
import base64
import time

# if __name__=='__main__':

input = sys.argv[1]

#print(input)

print("Job start")

content=base64.b64decode(input)

print("decode base64 done")

content = json.loads(content)

print("first json load done")

content = json.loads(content)

print("second json load done")

print(content)

print("Job done")

time.sleep(2)
