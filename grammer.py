import ply.lex as lex
import ply.yacc as yacc

from Module import Module
from Module import ParameterList

class Parser:
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

    
    def __init__(self):
        self.lexer  = lex.lex(module=self)
        self.parser = yacc.yacc(module=self)
        self.modules = []

    #t_ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    def t_ID(self,t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.type = Parser.reserved_map.get(t.value,'ID')
        return t
    
    def t_NUM(self,t):
        r'\d+'
        t.value = int(t.value)
        return t

    t_ignore = " \t"

    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")
    
    def t_error(self,t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

        
    def p_module_unit(self,p):
        '''module_unit : module ID '(' param_list ')' endmodule'''
        print "ID=", p[2]
        print "p[4]=", p[4]
        for param in p[4]:
            print param
        m = Module(p[2], ParameterList(p[4]))
        self.modules.append(m)

    def p_param_list_recursive(self,p):
        '''param_list : ID ',' param_list'''
        p[0] = [ p[1] ] + p[3]

    def p_param_list_id(self,p):
        '''param_list : ID'''
        p[0] = [1]

    def p_param_list_null(self,p):
        '''param_list : '''
        p[0] = []

    def p_error(self,p):
        if p:
            print("Syntax error at '%s'" % p.value)
        else:
            print("Syntax error at EOF")

    def parse(self, buf):
        self.parser.parse(buf)
        return self.modules


