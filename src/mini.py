#/bin/python3

import sys
from pyparsing import *

current = sys.modules[__name__]


symbols = ("A", "B", "(", ")")

for sym in symbols:
    setattr(current,sym,sym)

for prop in dir(current):
    print(prop)

with open("non_terminal_symbols.txt","r") as f:
    for line in f:
        print("\"{0}\"({1})".format(line.strip(),len(line)))

with open("keywords.txt","r") as f:
    for line in f:
        print("\"{0}\"({1})".format(line.strip("_\n"),len(line)))


