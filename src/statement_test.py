# -*- coding: utf-8 -*-
import sys
import unittest

from test_common import GrammarTestCase, TestCase
import pyparsing as pp
import grammar
import action

# @TestCase(grammar)
# def test_statement(self):
#     print(self.check_pass("A=B;").asXML())
#     # print(self.check_pass("A<=B;").asXML())

# @TestCase(grammar)
# def test_blocking_assignment(self):
#     print(self.check_pass("A=B").asXML())

# @TestCase(grammar)
# def test_nonblocking_assignment(self):
#     print(self.check_pass("A <= 1").asXML())
#     print(self.check_pass("A <=1").asXML())

#@TestCase(grammar)
# def test_procedural_continuous_assignments(self):
#     print(self.check_pass("assign hoge = 1").asXML())

@TestCase(grammar)
def test_conditional_statement(self):
    print(self.check_pass(" if ( ABC < 0) ;").asXML())
    print(self.check_pass(" if ( ABC < 0) A=B;").asXML())
    print(self.check_pass('''
if ( -1 < X )
     A = 0;
else 
     A = 2;
''').asXML())
    print(self.check_pass('''
if ( -1 < X )
     A = 0;
else  if ( 0 < X)
     A = 1;
else
     A = 2;
''').asXML())
    print(self.check_pass('''
if ( -1 < X )
     A = 0;
else  if ( 0 <= X)
     A = 1;
else  if ( 0 < X)
     A = 1;
else  if ( 0 < X)
     A = 1;
else  if ( 0 > X)
     A = 1;
else
     A = 2;
''').asXML())


    

#@TestCase(grammar)
# def test_expression(self):
#     print(self.check_pass("hoge < 2").asXML())

# @TestCase(grammar)
# def test_statement_or_null(self):
#     print(self.check_pass(";").asXML())

if __name__=='__main__':
    unittest.main()

    g = pp.Group(
        grammar.IF + grammar.LP + grammar.expression + grammar.RP + grammar.statement_or_null("name") 
        ) + pp.stringEnd

    def action():
        print("action")
    g.setParseAction(action)

    #result = g.parseString("if ;")
    result = g.parseString("if (A <2) ;")

    if result:
        print(result)
    else:
        print("NG")
