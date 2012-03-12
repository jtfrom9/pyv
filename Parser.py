# -*- coding: utf-8 -*-
import ply.lex as lex
import ply.yacc as yacc
from ply.lex import TOKEN

import grammer
import re


class Parser(grammer.Module, grammer.ModuleItem, grammer.Port, grammer.Variables,
             grammer.Expression, grammer.Statement,
             grammer.TaskAndFunction):
    # reserved words
    reserved = ('module', 'endmodule',
                'function', 'endfunction',
                'task', 'endtask',
                'begin', 'end',
                'assign',
                'initial',
                'always',
                'input', 'output', 'inout',
                'reg', 'wire',
                'integer',
                'for', 'if', 'else'
                )
    
    #reserved_map = { word:word for word in reserved }
    reserved_map = {}
    for word in reserved:
        reserved_map[word] = word

    # tokens
    tokens = ('ID', 'NUM', 'NB_ASIGN', 'STASK', 'STRING') + reserved

    # literals
    literals = "()[],.;:$=<+-"

    
    def __init__(self):
        self.lexer  = lex.lex(module=self)
        self.parser = yacc.yacc(module=self,start='module_definition')
        self.modules = []

    def parse(self, buf):
        self.parser.parse(buf)
        return self.modules

   
    #t_ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    def t_ID(self,t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.type = Parser.reserved_map.get(t.value,'ID')
        return t
    
    def t_NUM(self,t):
        r'\d+'
        t.value = int(t.value)
        return t

    t_NB_ASIGN = r'<='


    stask_pat = r'\$([a-zA-Z_][a-zA-Z0-9]*)'

    @TOKEN(stask_pat)
    def t_STASK(self,t):
        t.type = 'STASK'
        t.value = re.match(Parser.stask_pat,t.value).group(1)
        return t

    t_STRING = r'"[^"]*"'

    t_ignore = " \t"

    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")
    
    def t_error(self,t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

        
    def p_error(self,p):
        if p:
            print("Syntax error at '%s'" % p.value)
        else:
            print("Syntax error at EOF")

#     def p_empty(self,p):
#         '''empty : '''
#         pass
            
    precedence = (('left', 'INPUT_DECL', 'OUTPUT_DECL', 'INOUT_DECL')
                  ,('left', 'IDS')
                  ,('left', '+', '-')
                  ,('left', '*',)
                  ,('right', 'UNARY')
                  ,)

