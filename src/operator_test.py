# -*- coding: utf-8 -*-
import sys
import unittest

from test_common import GrammarTestCase, TestCase
import grammar
import action

@TestCase(grammar)
def test_unary_operator(self):
    self.check_pass("~|")
    self.check_pass("~^")
    self.check_pass("^~")

@TestCase(grammar)
def test_binary_operator(self):
    self.check_pass("|| ")
    self.check_pass("** ")
    self.check_pass("** ")

if __name__=='__main__':
    unittest.main()

