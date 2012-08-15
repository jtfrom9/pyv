# -*- coding: utf-8 -*-

import pyparsing as pp
import unittest
import pprint

import parser as p
from test_common import *

def action_unsigned_number(s,loc,tok):
    return int(tok[0])
p.unsigned_number.setParseAction(action_unsigned_number)
p.size.setParseAction(lambda t: int(t[0]))

def print_props(obj):
    for prop in dir(obj):
        print("{0} = {1}".format(prop,getattr(obj,prop)))

def action_number(s,l,tok):
    print("action_number")
    if tok.number[0].decimal_number:
        print("OK")
        #print(tok.number[0].decimal_number.asXML())
        pprint.pprint(tok.number[0].decimal_number)
    #print_props(tok.number[0].decimal_number)
    # print("  # of tok={0}".format(len(tok[0])))
    # for i,t in enumerate(tok[0]):
    #     print("    tok[{0}]={1} {2} {3}".format(i,t,type(t),dir(t)))
    #     print("             {0}".format(dir(t)))
p.number.setParseAction(action_number)


def action_real(s,l,tok):
    return float(s)
    print("action_real")
    print("  # of tok={0}".format(len(tok[0])))
    print("         s={0}".format(s))
    for i,t in enumerate(tok[0]):
        print("    tok[{0}]={1} {2}".format(i,t,type(t)))
#        print("             {0}".format(dir(t)))
    if len(tok[0])==2:
        return float(s)
    else:
        return float(s)
        # token=tok[0]
        # i=0
        # value = token[i]
        # i++
        # if type(token[i])==type(int):
        #     value = 

p.real_number.setParseAction(action_real)

@pp.traceParseAction
def action_decimal_number(s,l,tok):
    print("action_decimal_number")
    print("  # of tok={0}".format(len(tok[0])))
    print("         s={0}".format(s))
    for i,t in enumerate(tok[0]):
        print("    tok[{0}]={1} {2}".format(i,t,type(t)))
    #print(dir(tok[0]))
    # print("tok={0}".format(dir(tok)))
    # print("tok.decimal_number={0}".format(dir(tok.decimal_number)))
    # print("tok.decimal_number={0}".format(dir(tok[0])))
    # print("tok.decimal_number.size={0}".format(dir(tok.decimal_number.size)))
    # print("tok.decimal_number.unsi={0}".format(dir(tok.decimal_number.unsigned_number)))
    print(dir(tok.decimal_number.size))
    print(tok.asXML())
        
p.decimal_number.setParseAction(action_decimal_number)


# @TestCase(p)
# def test_unsigned_number(self):
#     self.check_pass('''  10''')
@TestCase(p)
def test_number(self):
    #self.check_pass('''  10''')
    #self.check_pass("1.0")
    self.check_pass("1e10")


if __name__=='__main__':
    result = p.number.parseString("20.03")
    print(result.asXML())
    result = p.number.parseString("20e30")
    print(result.asXML())
    result = p.number.parseString("20e+30")
    print(result.asXML())
    result = p.number.parseString("20.12e+30")
    print(result.asXML())
    result = p.number.parseString("1")
    print(result.asXML())
    result = p.number.parseString("10'd10")
    print(result.asXML())
    #unittest.main()
    
