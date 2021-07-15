import sys
import json
from pathlib import Path
import pathlib
import time


# if __name__=='__main__':

input = sys.argv[1]

txt = Path(input).read_text()
JsonF = json.loads(txt)

t = open('testingtext.txt','w')
t.write(JsonF['arch'])
t.close()