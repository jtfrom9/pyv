# -*- coding: utf-8 -*-
import sys
import unittest

from test_common import GrammarTestCase, TestCase
import grammar
import action



@TestCase(grammar)
def test_constant_function_call(self):
    print(self.check_pass("foo(1)").asXML())

@TestCase(grammar)
def test_constant_primary(self):
    print(self.check_pass("10").asXML())

# @TestCase(grammar)
# def test_constant_concatenation(self):
#     print(self.check_pass("{").asXML())

# @TestCase(grammar)
# def test_number(self):
#     print(self.check_pass("10").asXML())

if __name__=='__main__':
    unittest.main()
