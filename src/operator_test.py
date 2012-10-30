# -*- coding: utf-8 -*-
import sys
import unittest

from test_common import testOf
import grammar

@testOf(grammar.unary_operator)
def test_unary_operator(self):
    self.check_pass("~|")
    self.check_pass("~^")
    self.check_pass("^~")

@testOf(grammar.binary_operator)
def test_binary_operator(self):
    self.check_pass("|| ")
    self.check_pass("** ")
    self.check_pass("** ")

if __name__=='__main__':
    unittest.main()

