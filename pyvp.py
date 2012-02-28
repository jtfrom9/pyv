import ply.lex as lex
import ply.yacc as yacc

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


def p_module_unit(p):
    '''module_unit : module ID '(' param_list ')' endmodule'''
    print "ID=", p[2]
    for param in p[4]:
        print param

def p_param_list_recursive(p):
    '''param_list : ID ',' param_list
                  | ID
    '''
    p[0] = p[1]

def p_param_list_null(p):
    '''param_list : '''


def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")


# lexer.input('test.v')
# for line in lexer:
#     print line

parser = yacc.yacc()
for line in open('test3.v'):
    try:
        parser.parse(line)
    except EOFError:
        break
    

