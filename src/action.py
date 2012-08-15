# -*- coding: utf-8 -*-
from pyparsing import ParseFatalException
import unittest
import pprint
import math

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

def Action(grammar):
    def _decorator(action):
        func = GroupedAction(action)
        grammar.setParseAction(func)
        return func
    return _decorator

@Action(grammar.real_number)
def realNumberAction(s,l,token):
    return ast.Float(s)

@Action(grammar.decimal_number)
def decimalNumberAction(s, loc, token):
    def dval(vstr): 
        return int(vstr, ast.FixedWidthValue.Decimal)
    def s2val(width):
        val = int(token.unsigned_number)
        if val >= pow(2,width):
            print("Warning: constant {0} is truncate to {1} bit value: {2}".format(
                    s, width, pow(2,width)-1))
        return ast.State2Value(s,width,ast.FixedWidthValue.Decimal, val)
    def s4val(width,v):
        return ast.State4Value(s,width,ast.FixedWidthValue.Decimal, v*width)

    if len(token)==1:
        return s2val(32)
    else:
        width = token.size if token.size else 32
        if token.x_digit:
            return s4val(width,token.x_digit)
        if token.z_digit:
             return s4val(width,token.z_digit)
        if token.unsigned_number:
            return s2val(width)

def valueActions(name,vtype):
    @GroupedAction
    def _action(s,loc,token):
        width = token.size if token.size else 32
        value_token = getattr(token,name)
        trans = value_token.translate(None,'xXzZ?')
        if trans==value_token:
            return ast.State2Value(s,width,vtype,int(value_token,vtype))
        else:
            return ast.State4Value(s,width,vtype,value_token)
    return _action

grammar.binary_number.setParseAction (valueActions('binary_value' , ast.FixedWidthValue.Binary))
grammar.octal_number.setParseAction  (valueActions('octal_value'  , ast.FixedWidthValue.Octal))
grammar.hex_number.setParseAction    (valueActions('hex_value'    , ast.FixedWidthValue.Hex))

grammar.size.setParseAction                    (lambda t: int(t[0]))
grammar.non_zero_unsigned_number.setParseAction(lambda t: t[0])
grammar.unsigned_number.setParseAction         (lambda t: t[0])
grammar.binary_value.setParseAction            (lambda t: t[0])
grammar.octal_value.setParseAction             (lambda t: t[0])
grammar.hex_value.setParseAction               (lambda t: t[0])

    


