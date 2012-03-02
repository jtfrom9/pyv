from Module import Module
from Module import ParameterList

# reserved words
reserved = ('module', 'endmodule', 
            'task', 'endtask',
            'begin', 'end',
            'initial',
            'always',
            'input', 'output', 'inout',
            'reg', 'wire',
            'integer',
            'for', 'if')

#reserved_map = { word:word for word in reserved }
reserved_map = {}
for word in reserved:
    reserved_map[word] = word



# tokens
tokens = ('ID', 'NUM') + reserved

# literals
literals = "()[],.;:$"

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

