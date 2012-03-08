import grammer
from sys import argv

    
filename = 'test.v' if len(argv)==1 else argv[1]
file = open(filename)

parser = grammer.Parser()


print "------"
for m in parser.parse(file.read()):
    print "module = ", m.name()
    print "params = ", [p for p in m.param().params()]


