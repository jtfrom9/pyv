# -*- coding: utf-8 -*-
from pyparsing import *

num = Word( nums )
plus_exp =  num + "+" + num
plus_exp("pexp")

def action1(t):
    print("action1: {0}".format(t))
    #return [ t[0], t[2] ]

plus_exp.setParseAction(action1)

r = (plus_exp + stringEnd).parseString("1+1")
print(r)

exp_list = delimitedList( plus_exp )

r = (exp_list + stringEnd).parseString("1+1, 1+1")
print(r)

two_exp = plus_exp("before") + plus_exp("after")
def action2(t):
    print("action2: {0}".format(t))
    print("before = {0}".format(t.before))
    print("after = {0}".format(t.after))
two_exp.setParseAction(action2)

r = (two_exp + stringEnd).parseString("1+1  1+1")
print(r)


group_exp = Group( plus_exp )("before") + Group( plus_exp )("after")
r = (group_exp + stringEnd).parseString("1+1  1+1")
print(r.asXML())
print(r.asList())
print(r)


group_group_exp = Group( delimitedList( group_exp ) )("G")

def action3(t):
    print("action3: {0}".format(t))
    print("action3: {0}".format(t.G))
    #return [x for x in t.G]
    return t
     
group_group_exp.setParseAction(action3)

r = (group_group_exp + stringEnd).parseString("1+1  1+1, 2+2 3+3")
print(r)



