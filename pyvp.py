import ply.lex as lex
import ply.yacc as yacc
import grammer
from sys import argv

lexer = lex.lex(module=grammer)
parser = yacc.yacc(module=grammer)

data = open('test.v' if len(argv)==1 else argv[1]).read()

parser.parse(data)

print "------"
for m in grammer.modules:
    print "module = ", m.name()
    print "params = ", [p for p in m.param().params()]


