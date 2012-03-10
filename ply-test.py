import ply.lex as lex
import ply.yacc as yacc
from ply.lex import TOKEN
import re

class DummyLexer:
    def input(self, input):
        self.input_iter = iter(input)

    def token(self):
        try:
            tok = self.input_iter.next()
        except StopIteration:
            return None
        return tok
        

class Lexer:
    tokens = ['ID', 'NUM', 'STASK', 'STRING']
    literals = "()[],.;:$=<+-"

    t_ignore = ' ,\t'
    
    t_NUM = r'[\d]+'
    t_STRING = r'"[^"]*"'
    def t_ID(self,t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        return t

    stask_pat = r'\$([a-zA-Z_][a-zA-Z0-9]*)'

    @TOKEN(stask_pat)
    def t_STASK(self,t):
        t.type = 'STASK'
        t.value = re.match(Lexer.stask_pat,t.value).group(1)
        print t
        return t
    
    def t_error(self,t):
        print "error"

    def __init__(self):
        self._lex = lex.lex(module = self)
        
    def token(self):
        return self._lex.token()
    def input(self,buf):
        self._lex.input(buf)
    
def dump(lex, buf):
    i = 0
    lex.input(buf)
    while(True):
        tok = lex.token()
        if not tok: break
        print "[",i,"] ", tok
        i+=1

print "---"
dl =  DummyLexer()
dump(dl,"a b c d")
print "---"        
dump(dl,[1,2,3,4,5,6,7])
print "---"        
dump(Lexer(),"abc 123 f02,a,b, 123")



class TestParser:
    def __init__(self,lexer):
        self._lexer = lexer
        self.tokens = self._lexer.tokens
        self.parser = yacc.yacc(module=self, debug=1)
        
    def parse(self,buf):
        self.parser.parse(buf, lexer=self._lexer,debug=0)
        
    def p_exp(self,p):
        '''exp : term '+' term
               | stask
               | stask_call
          term : NUM
                | ID
        '''
        print [obj for obj in p]

    def p_stask(self,p):
        '''stask : STASK stask
        '''
        p[0] = [ p[1] ] + p[2]
        print [obj for obj in p]

    def p_stask2(self,p):
        '''stask : STASK 
        '''
        p[0] = [ p[1] ]
        print [obj for obj in p]

    def p_stask_call(self,p):
        '''stask_call : STASK '(' param ')'
        '''
        print [obj for obj in p]

    def p_param(self,p):
        '''param : ID
                 | NUM
        '''
        p[0] = p[1]
        
    def p_error(self,p):
        if p:
            print("error at '%s'" % p.value)

    def restart(self):
        self.parser.restart()
            
p = TestParser(Lexer())
p.parse("1+a")
print "----"
p.restart()
p.parse("$include $define")
p.parse("$include(10)")
p.parse("$include(A)")


# tokens = ['ID', 'NUM']
# def p_exp(p):
#     '''exp : exp '+' exp
#     | NUM
#     | ID
#     '''
#     print [obj for obj in p]
    
# def p_error(p):
#     if p:
#         print("Syntax error at '%s'" % p.value)
#     else:
#         print("Syntax error at EOF")

# parser = yacc.yacc(debug=0)
# parser.parse("1+2",lexer=Lexer())


