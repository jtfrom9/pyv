# -*- coding: utf-8 -*-
import sys
import unittest

from test_common import GrammarTestCase, TestCase2, _print
from pyparsing import stringEnd
import grammar
import action

@TestCase2(grammar.concatenation)
def test102(self):
    _print(self.check_pass("{1,1}"))
    _print(self.check_pass("{1+2,3}"))
    _print(self.check_pass("{1+2,3,X}"))
    _print(self.check_pass("{1+2,3,X,A[1]}"))
    _print(self.check_fail("{1,1,}")) 

@TestCase2(grammar.constant_concatenation)
def test103(self):
    pass


@TestCase2(grammar.constant_multiple_concatenation)
def test104(self):
    pass


@TestCase2(grammar.module_path_concatenation)
def test105(self):
    pass


@TestCase2(grammar.module_path_multiple_concatenation)
def test106(self):
    pass


@TestCase2(grammar.multiple_concatenation)
def test107(self):
    pass


@TestCase2(grammar.net_concatenation)
def test108(self):
    pass


@TestCase2(grammar.net_concatenation_value)
def test109(self):
    _print(self.check_pass("foo.bar.hoge[5].A[1]"))
    _print(self.check_pass("foo.bar.hoge[5].A[1][1]"))
    _print(self.check_pass("foo.bar.hoge[5].A[1][X]"))
    _print(self.check_pass("foo.bar.hoge[5].A[1][X][y]"))
    _print(self.check_pass("foo.bar.hoge[5].A[1][X][3:1]"))
    #_print(self.check_pass("10"))



@TestCase2(grammar.variable_concatenation)
def test110(self):
    pass

if __name__=='__main__':
    unittest.main()
