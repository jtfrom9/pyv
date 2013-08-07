# -*- coding: utf-8 -*-
import sys
import unittest

from test_common import testOf, grammar

@testOf(grammar.unary_operator)
def test_unary_operator(self):
    self.try_parse_pass("~|")
    self.try_parse_pass("~^")
    self.try_parse_pass("^~")

@testOf(grammar.binary_operator)
def test_binary_operator(self):
    self.try_parse_pass("|| ")
    self.try_parse_pass("** ")
    self.try_parse_pass("** ")

if __name__=='__main__':
    unittest.main()

