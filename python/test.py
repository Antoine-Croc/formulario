import sys
import json
from pathlib import Path
import pathlib
import time


# if __name__=='__main__':

input = sys.argv[1]

txt = Path('getmeoutofhere.txt').read_text()
t = open("testingtext.txt", 'x')
t.write(txt)
t.close()