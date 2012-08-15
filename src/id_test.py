# -*- coding: utf-8 -*-
import sys
import unittest

from test_common import GrammarTestCase, TestCase
import grammar
import action


# @TestCase(grammar)
# def test_identifier(self):        
#     print(self.check_pass("hoge").asXML())

@TestCase(grammar)
def test_simple_identifier(self):        
    print(self.check_pass("hoge").asXML())

# @TestCase(grammar)
# def test_simple_arrayed_identifier(self):        
#     print(self.check_pass("hoge[10:5]").asXML())

@TestCase(grammar)
def test__range(self):
    print(self.check_pass("[10:5]").asXML())

if __name__=='__main__':
    unittest.main()
