import ply.lex as lex
import ply.yacc as yacc
import re
import sys
from sys import argv

reserved = ('::=')
literals = "()[],.-+;:|#\""

tokens = ('IDENTIFIER',) + reserved

t_IDENTIFIER = r'[a-zA-Z][a-zA-Z0-9_]*'

def p_input(p):
    '''input : definitions'''
    pass

def p_definitions(p):
    '''definitions : definition definitions
                   | definitions'''
    pass

def p_definition(p):
    '''definition : IDENTIFIER ::= conditions
                  | chapter
    '''   
    pass

def p_conditions(p):
    '''conditions : condition | conditions'''
    pass

def p_condition_single(p):
    '''condition : NODE'''
    pass

def p_condition_multi(p):
    '''condition : NODE condition'''
    pass

def p_condition_recursive(p):
    '''condition : '{' condition '}'''
    pass

def p_condition_optional(p):
    '''condition  '[' condition ']' '''
    pass


def p_special_simbol(p):
    '''special_simbol : '#'
                      | '|'
                      | '+'
                      | '-'
                      | ';'
                      | ':'
                      | '"'
    '''
    pass


def testIDENTIFIER(str):
    m = re.search(t_IDENTIFIER, str)
    sys.stdout.write('\'' + str + '\'  ... ')
    if not m:
        sys.stdout.write("* NOT MATCH*")
    else:
        sys.stdout.write(m.group(0))
    sys.stdout.write('\n')
    
if __name__ == '__main__':
    #print tokens
    testIDENTIFIER('::=')
    testIDENTIFIER('hoge')
    testIDENTIFIER('|')
    


    
