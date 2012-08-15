# -*- coding: utf-8 -*-
from pyparsing import ParseFatalException
import unittest
import pprint

import grammar
import ast
from test_common import *

def GroupedAction(action):
    # def _decorator_(*args):
    #     string=None
    #     loc=None
    #     tokens=None
    #     print("GroupedAction: # of args={0}".format(len(args)))
    #     for i,arg in enumerate(args):
    #         print(" arg[{0}]={1}".format(i, arg))
    #     if len(args)==3:
    #         string = args[0]
    #         loc    = args[1]
    #         tokens = args[2]
    #     elif (len(args)==2):
    #         loc    = args[0]
    #         tokens = args[1]
    #     elif len(args)==1:
    #         tokens = args[0]
    #     action(string, loc, tokens[0])
    def _decorator(string,loc,tokens):
        try:
            return action(string, loc, tokens[0])
        except Exception, e:
            raise ParseFatalException(string, loc, 
                                      "parse action \'{0}\' throw an exception: {1}".format(action.__name__, e))
    return _decorator


grammar.real_number.setParseAction(lambda s,l,t: Float(s))

@GroupedAction
def decimalAction(s, loc, token):
    def dval(vstr): 
        return int(vstr, ast.FixedWidthValue.Decimal)
    def s2val(width):
        return ast.State2Value(s,width,ast.FixedWidthValue.Decimal, int(token.unsigned_number))
    def s4val(width,v):
        return ast.State4Value(s,width,ast.FixedWidthValue.Decimal, v*width)

    if len(token)==1:
        return s2val(32)
    else:
        if token.x_digit:
            return s4val(token.size,token.x_digit)
        if token.z_digit:
             return s4val(token.size,token.z_digit)
        if token.unsigned_number:
            return s2val(token.size)

grammar.decimal_number.setParseAction(decimalAction)

grammar.non_zero_unsigned_number.setParseAction(lambda t: t[0])
grammar.unsigned_number.setParseAction         (lambda t: t[0])
grammar.size.setParseAction(                    lambda t: int(t[0]))


@TestCase(grammar)
def test_decimal_number(self):
    print(self.check_pass("1'd5").asXML())
    print(self.check_pass("10'dx").asXML())
    print(self.check_pass("1'd?").asXML())
    print(self.check_pass("20").asXML())


if __name__=='__main__':
    unittest.main()

