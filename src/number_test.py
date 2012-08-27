# -*- coding: utf-8 -*-
import sys
import unittest

from test_common import GrammarTestCase, TestCase, _print
import grammar
import action

@TestCase(grammar)
def test_number(self):
    _print(self.check_pass("23.5"))
    _print(self.check_pass("1.0e+1"))
    _print(self.check_pass("0.0E-30"))
    _print(self.check_pass("0.0"))
    _print(self.check_pass("123"))
    _print(self.check_pass("01"))
    _print(self.check_pass("'d0"))
    _print(self.check_pass("5'd0"))

if __name__=='__main__':
    unittest.main()
