import ply.lex as lex

class DummyLexer:
    def __init__(self, input):
        self.input_iter = iter(input)

    def token(self):
        try:
            tok = self.input_iter.next()
        except StopIteration:
            return None
        return tok
        

class Lexer:
    tokens = ['ID', 'NUM']
    
    t_ignore = ' ,\t'
    
    t_NUM = r'[\d]+'
    def t_ID(self,t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        return t
        
    def t_error(self,t):
        print "error"

    def __init__(self, input):
        self._lex = lex.lex(module = self)
        self._lex.input(input)
        
    def token(self):
        return self._lex.token()

    
def dump(lex):
    i = 0
    while(True):
        tok = lex.token()
        if not tok: break
        print "[",i,"] ", tok
        i+=1

print "---"        
dump(DummyLexer("a b c d"))
print "---"        
dump(DummyLexer([1,2,3,4,5,6,7]))

print "---"        
dump(Lexer("abc 123 f02,a,b, 123"))




    
