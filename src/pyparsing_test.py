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
print("one={0}".format(result.id[0].one))
print("two={0}".format(result.id[0].two))
