# -*- coding: utf-8 -*-
import pyparsing as pp
import unittest
import pprint

import parser as p
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
            raise pp.ParseFatalException(string, loc, 
                                      "parse action \'{0}\' throw an exception: {1}".format(action.__name__, e))
    return _decorator


p.real_number.setParseAction(lambda s,l,t: Float(s))

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

p.decimal_number.setParseAction(decimalAction)

p.non_zero_unsigned_number.setParseAction(lambda t: t[0])
p.unsigned_number.setParseAction         (lambda t: t[0])
p.size.setParseAction(                    lambda t: int(t[0]))


@TestCase(p)
def test_decimal_number(self):
    print(self.check_pass("1'd5").asXML())
    print(self.check_pass("10'dx").asXML())
    print(self.check_pass("1'd?").asXML())
    print(self.check_pass("20").asXML())


if __name__=='__main__':
    # for gen in p.number.scanString("1"):
    #     print(type(gen))
    unittest.main()

    # #result = p.decimal_number.parseString("1'd5")
    # result = p.decimal_number.parseString("1'd?")
    # #result = p.decimal_number.parseString("1")
    # print(result.asXML())

    # print(type(result))
    # print(dir(result))
    # print(type(result.decimal_number))
    # print(dir(result.decimal_number))
    # print("result={0}".format(result.decimal_number))

    # print(result.decimal_number[0].size)
    # print(result.decimal_number[0].decimal_base)
    # print(result.decimal_number[0].unsigned_number)
