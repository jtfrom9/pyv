# -*- coding: utf-8 -*-
from __future__ import print_function

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
    def _decorator(_s,loc,tokens):
        result = None
        #print(">> enter {0}: l={1}, token={2}".format(action.__name__, loc, tokens[0]))
        try:
            result = action(_s, loc, tokens[0])
        except Exception as e:
            raise ParseFatalException(_s, loc, 
                                      "parse action \'{0}\' throw an exception: {1}".format(action.__name__, e))
        #print("<< exit  {0}: ret={1}".format(action.__name__, result))
        return result
    return _decorator

def Action(grammar):
    def _decorator(action):
        func = GroupedAction(action)
        grammar.setParseAction(func)
        return func
    return _decorator


# A.2.5 Declaration ranges

@Action(grammar._range)
def rangeAction(_s,loc,token):
    # print("rangeAction: s={0}, loc={1}, token={2}".format(s,loc,token))
    # print("msb_constant_expression={0}".format(token.msb_constant_expression.asXML()))
    # print("lsb_constant_expression={0}".format(token.lsb_constant_expression))
    try:
        if not token.msb_constant_expression:
            raise Exception("1")
        if not token.msb_constant_expression.constant_expression:
            raise Exception("2")
        if not token.msb_constant_expression.constant_expression[0].constant_primary:
            raise Exception("3")
        if not token.msb_constant_expression.constant_expression[0].constant_primary[0].number:
            raise Exception("4")
    except Exception as msg:
        print("_range Not Implemented completely: {0}".format(msg))
        assert False
    return ast.Range(token.msb_constant_expression.constant_expression[0].constant_primary[0].number,
                     token.lsb_constant_expression.constant_expression[0].constant_primary[0].number)

class Expression(ast.AstNode):
    #def __init__(self, constant):
    def __init__(self):
        pass

class Primary(Expression):
    def __init__(self, obj):
        self.obj = obj
    def longName(self):
        data = None
        if isinstance(self.obj,tuple):
            head = self.obj[0]
            data = str(head[0])
        elif isinstance(self.obj, ast.Numeric):
            data = str(self.obj)
        else:
            print(type(self.obj))
            assert False
        return "({0} {1})".format(self.__class__.__name__,data)

class UnaryExpression(Expression):
    def __init__(self, op, exp):
        self.op = op
        self.exp = exp
    def longName(self):
        return "({0} {1})".format(self.op, self.exp)

class BinaryExpression(Expression):
    def __init__(self,op,left,right):
        self.op   =op
        self.lexp = left
        self.rexp = right
    def longName(self):
        return "({0} {1} {2})".format(self.op, self.lexp[0], self.rexp[0])

# A.8.3 Expressions

@Action(grammar.expression)
def expressionAction(_s,l,token):
    if token.unary_operator:
        return UnaryExpression(token.unary_operator, token.primary)
    elif token.binary_operator:
        return BinaryExpression(token.binary_operator, token[0], token[2])
    elif token.primary:
        return token
    else:
        raise Exception("Not Implemented completely expressionAction: token={0}".format(token))
    
# A.8.4 Primaries

@Action(grammar.primary)
def primaryAction(_s,l,token):
    if token.number:
        return Primary(token.number[0])
    elif token.hierarchical_identifier:
        exp  = token.expression[0] if token.expression else None
        rexp = token.range_expression[0] if token.range_expression else None
        return Primary((token.hierarchical_identifier[0], exp, rexp))
    elif token.function_call:
        pass
    else:
        raise Exception("Not Implemented completely primaryAction: token={0}".format(token))




# A.8.7 Numbers

@Action(grammar.number)
def numberAction(_s,l,token): 
    return token

@Action(grammar.real_number)
def realNumberAction(_s,l,token):
    return ast.Float(token)    # TODO: fixme

@Action(grammar.decimal_number)
def decimalNumberAction(_s, loc, token):
    def dval(vstr): 
        return int(vstr, ast.FixedWidthValue.Decimal)
    def s2val(width):
        val = int(token.unsigned_number)
        if val >= pow(2,width):
            print("Warning: constant {0} is truncate to {1} bit value: {2}".format(
                    token.unsigned_number, width, pow(2,width)-1))
        return ast.State2Value(token.unsigned_number,width,ast.FixedWidthValue.Decimal, val)
    def s4val(width,v):
        return ast.State4Value(v,width,ast.FixedWidthValue.Decimal, v*width)

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
    def _action(_s,loc,token):
        width = token.size if token.size else 32
        vstr = getattr(token,name)
        trans = vstr.translate(None,'xXzZ?')
        if trans==vstr:
            return ast.State2Value(vstr,width,vtype,int(vstr,vtype))
        else:
            return ast.State4Value(vstr,width,vtype,vstr)
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


# A.9.3 Identifiers
@Action(grammar.simple_identifier)
def simpleIdentifierAction(_s,loc,token):
    return ast.BasicId(token)

@Action(grammar.identifier)
def identifierAction(_s,loc,token):
    if token.simple_identifier:
        return token.simple_identifier
    elif token.escaped_identifier:
        return token.escaped_identifier
    else:
        assert False

@Action(grammar.simple_arrayed_identifier)
def simpleArrayedIdentifierAction(_s,loc,token):
    print(__name__)
    print(token.simple_identifier)
    if token._range:
        return ast.RangedId(token.simple_identifier.shortName(), token._range)
    else:
        return ast.BasicId(token.simple_identifier.shortName())

@Action(grammar.arrayed_identifier)
def arrayedIdentifierAction(_s,loc,token):
    if token.simple_arrayed_identifier:
        return token.simple_arrayed_identifier
    elif token.escaped_arrayed_identifier:
        return token.escaped_arrayed_identifier
    else:
        assert False
    
@Action(grammar.simple_hierarchical_branch)
def simpleHierarchicalBranchAction(_s,loc,token):
    index = None
    if token.index:
        index = int(token.index)
    ids=[]
    for node in token.nodes:
        if node.index:
            ids.append(ast.IndexedId(node.name[0], int(node.index)))
        else:
            ids.append(ast.BasicId(node.name[0]))
    return ast.HierarchicalId(token.simple_identifier, index, ids)

@Action(grammar.simple_hierarchical_identifier)
def simpleHierarchicalIdnetifierAction(_s,loc,token):
    if not token.escaped_identifier:
        return token
    else:
        assert isinstance(token, HierarchicalId)
        token.addId(ast.BasicId(token.escaped_identifier))
        
