import sys
import ply.lex as lex

reserved = ['if', 'foo']

tokens = reserved + ['ID', 'NUM']

t_NUM = r'\d+'

reserved_map = {}
for r in reserved:
    reserved_map[r] = r;

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved_map.get(t.value,'ID')
    return t

def t_error(t):
    print "error"

t_ignore = ' \t'

lexer = lex.lex()
lexer.input("a b if 1 23 f13 foo hoge ")

for token in lexer:
    print token



