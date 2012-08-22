# -*- coding: utf-8 -*-
import sys
import unittest

from test_common import GrammarTestCase, TestCase
import grammar
import action



# @TestCase(grammar)
# def test_constant_function_call(self):
#     print(self.check_pass("foo(1)").asXML())

# @TestCase(grammar)
# def test_constant_primary(self):
#     print(self.check_pass("10").asXML())

# @TestCase(grammar)
# def test_constant_concatenation(self):
#     print(self.check_pass("{").asXML())

# @TestCase(grammar)
# def test_number(self):
#     print(self.check_pass("10").asXML())


@TestCase(grammar)
def test_constant_range_expression(self):
    print(self.check_pass("1:0").asXML())
    
@TestCase(grammar)
def test_constant_expression(self):
#    print(self.check_pass("func()").asXML())
    print(self.check_pass("A").asXML())
    
@TestCase(grammar)
def test_net_lvalue(self):
#    print(self.check_pass("hoge").asXML())
    print(self.check_pass("hoge.foo[1:0]").asXML())
    print(self.check_pass("hoge.foo[0][1][2][1:0]").asXML())


@TestCase(grammar)
def test_expression(self):
    print(self.check_pass("A+10").asXML())
    print(self.check_pass("-X").asXML())
    print(self.check_pass("-X+10+A").asXML())

# @TestCase(grammar)
# def test_function_call(self):
#     print(self.check_pass("hoge(a)").asXML())
    # result = self.check_pass("hoge(a)")
    # for p in dir(result):
    #     prop = getattr(result,p)
    #     #print(prop)
    #     print("prop={0}, value={1}".format(p,str(prop)))


if __name__=='__main__':
    unittest.main()
