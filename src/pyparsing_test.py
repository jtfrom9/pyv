# -*- coding: utf-8 -*-
from pyparsing import *

class One(object):
    pass

one = Group(Literal("one"))("one").setParseAction(lambda t: 1)
two = Group(Literal("two"))("two")

class ID(object):
    pass

id = Forward()("id")
id << Group( one |
             two )

result = id.parseString("two")
print(result.asXML())
print(type(result))
print(type(result.id))
# print("one={0}".format(result.id[0].one))
# print("two={0}".format(result.id[0].two))


# import grammar
# sd = grammar.simple_identifier("name")
# def action(t):
#     print("t.simple_identifier={0}".format(t.simple_identifier))
#     print("type(t.simple_identifier))={0}".format(type(t.simple_identifier)))
#     print("t.name={0}".format(t.name))
#     print("type(t.name)={0}".format(type(t.name)))
# sd.setParseAction(action)
# sd.parseString("hoge")

ab_grammar = Forward()
C_grammar = Forward()
D_grammar = Forward()
E_grammar = Forward()

a_grammar = Literal("a")
b_grammar = Literal("b")
ab_grammar << Group(OneOrMore(a_grammar | b_grammar))("AB")

result = (ab_grammar+stringEnd).parseString("a b")
print(dir(result))

C_grammar << Group( "(" + ab_grammar + ")" )("C")
result = (C_grammar+stringEnd).parseString("( a a b ) ")
print(result.asXML())


D_grammar << Group( "(" + ab_grammar("hoge") + ")" )("D")
E_grammar << Group( "(" + ab_grammar("hoge") + ")" )("E")
F_grammar = Group( D_grammar | E_grammar )

def action(t):
    return "ab_grammar!"
ab_grammar.setParseAction(action)


result = (F_grammar+stringEnd).parseString("( a a b ) ")
print(result.asXML())
