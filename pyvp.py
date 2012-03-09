from sys import argv

import Parser
    
filename = 'test.v' if len(argv)==1 else argv[1]
file = open(filename)

parser = Parser.Parser()


print "------"
for m in parser.parse(file.read()):
    print "module = ", m.name()
    print "params = ", [p for p in m.param().params()]


