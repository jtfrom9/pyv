import parser as p
import pyparsing as pp
import sys

import unittest
from test_common import GrammarTestCase, TestCase

@TestCase(p)
def test_unary_operator(self):
    self.check_pass("~|")
    self.check_pass("~^")
    self.check_pass("^~")

@TestCase(p)
def test_binary_operator(self):
    self.check_pass("|| ")
    self.check_pass("** ")
    self.check_pass("** ")

if __name__=='__main__':
    unittest.main()

