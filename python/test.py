import sys
import json
from pathlib import *
import pathlib
import base64
import time

# if __name__=='__main__':

input = sys.argv[1]
content = json.loads(json.loads(base64.b64decode(input)))

print("Job start")
print(content)
print("Job done")
time.sleep(2)
