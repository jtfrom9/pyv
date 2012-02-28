import ply.lex as lex
import ply.yacc as yacc
from sys import argv

# reserved words
reserved = ('module', 'endmodule')

#reserved_map = { word:word for word in reserved }
reserved_map = {}
for word in reserved:
    reserved_map[word] = word

# tokens
tokens = ('ID', 'NUM') + reserved

# literals
literals = "(),"

#t_ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved_map.get(t.value,'ID')
    return t


def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# data='''
# hoge 123 
#  module ABC1
#  ab3
# '''

lexer = lex.lex()

# lexer.input(data)
# for tok in lexer:
#     print tok


class ParameterList:
    def __init__(self,param_list):
        self.__params = param_list

    def params(self):
        for p in self.__params:
            yield p

class Module:
    def __init__(self,name,param):
        self.__name = name
        self.__param = param

    def name(self):
        return self.__name

    def param(self):
        return self.__param


modules = []

def p_module_unit(p):
    '''module_unit : module ID '(' param_list ')' endmodule'''
    print "ID=", p[2]
    print "p[4]=", p[4]
    for param in p[4]:
        print param
    m = Module(p[2], ParameterList(p[4]))
    modules.append(m)

def p_param_list_recursive(p):
    '''param_list : ID ',' param_list'''
    p[0] = [ p[1] ] + p[3]

def p_param_list_id(p):
    '''param_list : ID'''
    p[0] = [1]

def p_param_list_null(p):
    '''param_list : '''
    p[0] = []

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")


# lexer.input('test.v')
# for line in lexer:
#     print line

parser = yacc.yacc()
data = open('test.v' if len(argv)==1 else argv[1]).read()

parser.parse(data)

print "------"
for m in modules:
    print "module = ", m.name()
    print "params = ", [p for p in m.param().params()]


