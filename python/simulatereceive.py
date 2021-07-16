import sys
import json
from pathlib import Path
import time

input = sys.argv[1]
if __name__=='__main__':

    time.sleep(10)

    txt = Path('../jsonfiles/'+input).read_text()
    JsonF = json.loads(txt)
    nameexit='../jsonfiles/finished'+input
    t = open(nameexit,'w')
    t.write(JsonF['arch'])
    t.close()