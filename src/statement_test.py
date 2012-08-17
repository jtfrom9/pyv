# -*- coding: utf-8 -*-
import sys
import unittest

from test_common import GrammarTestCase, TestCase
import pyparsing as pp
import grammar
import action

@TestCase(grammar)
def test_statement(self):
    print(self.check_pass("A=B;").asXML())
    # print(self.check_pass("A<=B;").asXML())

# @TestCase(grammar)
# def test_blocking_assignment(self):
#     print(self.check_pass("A=B").asXML())

# @TestCase(grammar)
# def test_nonblocking_assignment(self):
#     print(self.check_pass("A <= 1").asXML())
#     print(self.check_pass("A <=1").asXML())

@TestCase(grammar)
def test_procedural_continuous_assignments(self):
    print(self.check_pass("assign hoge = 1").asXML())

@TestCase(grammar)
def test_conditional_statement(self):
    print(self.check_pass(" if ( ABC < 0);").asXML())

@TestCase(grammar)
def test_expression(self):
    print(self.check_pass("hoge < 2").asXML())

@TestCase(grammar)
def test_statement_or_null(self):
    print(self.check_pass(";").asXML())

if __name__=='__main__':
    unittest.main()

    # g = (grammar.IF + grammar.LP + grammar.expression + grammar.RP + grammar.statement_or_null + pp.stringEnd)
    # result = g.parseString("if (A <2) ;")
    # print(result)
