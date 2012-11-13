# -*- coding: utf-8 -*-
import sys

from pyparsing import (Keyword, Literal, Regex, Regex, MatchFirst, NotAny, CharsNotIn, Suppress, 
                       Forward, Group, Optional, ZeroOrMore, OneOrMore, 
                       delimitedList, operatorPrecedence, opAssoc, oneOf,
                       ParseBaseException,
                       ParseResults)

self = sys.modules[__name__]

with open("keywords.txt","r") as f:
    _keywords = [line.strip() for line in f]

#ID = ~MatchFirst([Keyword(w) for w in _keywords]) + Word(alphas+'_', alphanums+'_')("id")
ID = ~MatchFirst([Keyword(w) for w in _keywords]) + Regex(r"[a-zA-Z_][a-zA-Z0-9_$]*")("id")
LP,RP,LB,RB,LC,RC,COLON,SEMICOLON,CAMMA,PERIOD,SHARP,EQUAL,AT,ASTA,Q,PLUS,MINUS,USC,APS = map(Suppress,("()[]{}:;,.#=@*?+-_'"))

NB = Suppress(Literal("<="))
TRIG = Suppress(Literal("->"))

#LP/RP : left/right paren          ()
#LB/RB : left/right bracket        []
#LC/RC : left/right curly bracket  {}

for kw in _keywords:
    setattr(self, kw.swapcase(), Keyword(kw)("keyword"))

with open("non_terminal_symbols.txt","r") as f:
    for name in (line.strip() for line in f):
        sym = Forward()(name)
        sym.enablePackrat()
        setattr(self, name, sym)

def alias(grammar, name):
    if name: 
        return Group(grammar)(name)
    else:
        return Group(grammar)

def _group(expr, err=None):
    class WrapGroup(Group):
        def __init__(self, expr):
            super(WrapGroup,self).__init__(expr)
        def parseImpl(*args):
            self = args[0]
            try:
                return super(WrapGroup,self).parseImpl(*(args[1:]))
            except ParseBaseException,pbe:
                pbe.msg = "Syntax Error: " + err
                raise
    return WrapGroup(expr)

def delim(expr,name=None,delimiter=','):
    g = _group( delimitedList(expr,delimiter) - NotAny(delimiter),
                err = "invalid ','" )
    return g(name) if name else g

def unalias(token): return token[0]
def ungroup(token): return token[0]

# def GroupedAction(action):
#     import inspect
#     try:
#         frame = inspect.currentframe(2)
#     except ValueError as e:
#         return None
#     else:
#         filename = frame.f_code.co_filename
#         lineno   = frame.f_lineno
#     def _decorator(_s,loc,token):
#         result = None
#         try:
#             result = action(_s, loc, token)
#         except Exception as e:
#             raise ParseFatalException(_s, loc, 
#                                       "\n  File \"{filename}\", line {lineno}\n    {reason}".
#                                       format(action   = action.__name__,
#                                              filename = filename,
#                                              lineno   = lineno,
#                                              reason   = e))
#         return result
#     return _decorator

def actionOf(*argv):
    def _decorator(action):
        for grammar in argv:
            grammar.setParseAction(action)
        return action
    return _decorator

def Grammar(expr_def):
    expr, action = expr_def()
    grammar = getattr(sys.modules[__name__], expr_def.__name__)
    grammar << expr
    grammar.setParseAction(action)
    return grammar

def GrammarNotImplementedYet(expr_def):
    expr = expr_def()[0]
    def _error():
        raise Exception("Not Implemented: " + expr_def.__name__)
    grammar = getattr(sys.modules[__name__], expr_def.__name__)
    grammar << expr
    grammar.setParseAction(_error)
    return grammar
    
