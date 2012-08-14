# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

import pyparsing as pp
import unittest
import pprint

import parser as p
from test_common import *

def GroupedAction(action):
    def _decorator(*args):
        string=None
        loc=None
        tokens=None
        print("args={0}".format(args))
        print("len={0}".format(len(args)))
        if len(args)==3:
            string = args[0]
            loc    = args[1]
            tokens = args[2]
            action(string, loc, tokens[0])
        elif (len(args)==2):
            loc    = args[0]
            tokens = args[1]
            action(string, loc, tokens[0])
        elif len(args)==1:
            tokens = args[0]
            action(string, loc, tokens[0])

    return _decorator

class Numeric(object):
    def __init__(self, string):
        self.string = string
    def __repr__(self):
        return self.string

class FixedWidth(Numeric):
    Binary = 2
    Octal  = 8
    Hex    = 16
    Decimal = 10

    def __init__(self, string, width, vtype):
        self.string = string
        self.width  = width
        self.vtype  = vtype

class State2Value(FixedWidth):
    def __init__(self, string, width, vtype):
        super(State2Value,self).__init__(string,width,vtype)
        print("string={0}, vtype={1}".format(string,vtype))
        self.vale = int(string,vtype)

class State4Value(FixedWidth):
    def __init__(self, string, width, vtype, bits):
        super(State4Value,self).__init__(string,width,vtype)
        self.bits = bits

class Float(Numeric):
    def __init__(self, string):
        super(Float,self).__init__(string)
        self.value = float(string)
    def __repr__(self):
        return self.value


p.real_number.setParseAction(lambda s,l,t: Float(s))

@GroupedAction
def decimalAction(string, loc, token):
    print("string={0}".format(string))
    print("len={0}".format(len(token)))
    print("dir={0}".format(dir(token)))
    print("token={0}".format(token))
    if len(token)==1:
        return State2Value(token.unsigned_number,32,FixedWidth.Decimal)
    else:
        if token.size: 
            width = token.size 
        else:
            width = 32 # temp
        if token.x_digit:
            return State4Value(string,width,FixedWidth.Decimal,string) #temp
        if token.z_digit:
            return State4Value(string,width,FixedWidth.Decimal,string) #temp
        if token.unsigned_number:
            print("OK")
            print("={0}".format(token.unsigned_number))
            return State2Value(token.unsigned_number,width,FixedWidth.Decimal,string) #temp

p.decimal_number.setParseAction(decimalAction)

def decimal(s,l,t): return t[0]
p.non_zero_unsigned_number.setParseAction(decimal)
p.unsigned_number.setParseAction(decimal)


if __name__=='__main__':
    # for gen in p.number.scanString("1"):
    #     print(type(gen))
    #unittest.main()

    # print(p.unsigned_number.parseString("1").asXML())
    # print(p.non_zero_unsigned_number.parseString("1").asXML())
    # result = p.decimal_number.parseString("1")
    # print(result.asXML())
    result = p.decimal_number.parseString("1'd5")
    print(result.asXML())
    # print("={0}".format(dir(result)))
    # print("={0}".format(dir(result.decimal_number)))
    # print("={0}".format(dir(result.decimal_number[0])))
    # print("={0}".format(result.decimal_number[0]))
    # print("={0}".format(dir(result.decimal_number[0].unsigned_number)))

    print(result.decimal_number[0].size)
    print(result.decimal_number[0].decimal_base)
    print(result.decimal_number[0].unsigned_number)
    
    
