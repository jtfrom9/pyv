# -*- coding: utf-8 -*-
import sys
import unittest

from test_common import GrammarTestCase, TestCase2, _print, run_tests
import grammar
import action

grammar.constant_primary.enablePackrat()

@TestCase2(grammar.constant_primary)
def test131(self):
    _print(self.check_pass("1"))
    _print(self.check_pass("{1,2,3}"))
    _print(self.check_pass("(1)"))
    _print(self.check_pass("({1,2,3})"))
    _print(self.check_pass("func(0,1,2)"))
    _print(self.check_pass("func(0?1:2)"))
    _print(self.check_pass("{{{{1}}}}"))
    _print(self.check_fail("A"))
    
@TestCase2(grammar.module_path_primary)
def test132(self):
    pass

@TestCase2(grammar.primary)
def test133(self):
    _print(self.check_pass("10"))
    _print(self.check_pass("foo(1)"))
    _print(self.check_pass("$display(a,b,c)"))
    _print(self.check_pass("foo.bar.hoge[5].A[1]"))
    _print(self.check_pass("foo.bar.hoge[5].A[1][1:0]"))
    _print(self.check_pass("foo.bar.hoge[5].A[1][X]"))
    _print(self.check_pass("foo.bar.hoge[5].A[1][X][y]"))
    _print(self.check_pass("foo.bar.hoge[5].A[1][X][3:1]"))
    _print(self.check_pass("{1,2,3}"))
    _print(self.check_pass("(10)"))

@TestCase2(grammar.net_lvalue)
def test134(self):
    _print(self.check_pass("A"))
    _print(self.check_pass("A[1:0]"))
    _print(self.check_pass("A[1]"))
    _print(self.check_pass("A[1][2]"))
    _print(self.check_fail("A[1][2][X]"))
    _print(self.check_pass("A[foo()][0][5:3]"))
    _print(self.check_pass("hoge.foo[1:0]"))
    _print(self.check_pass("hoge.foo[0][1][2][1:0]"))
    _print(self.check_fail("{1}"))
    _print(self.check_pass("{A,B}"))
    _print(self.check_pass("{{A,B},X,f}"))

@TestCase2(grammar.variable_lvalue)
def test135(self):
    _print(self.check_pass("A"))
    _print(self.check_pass("A[1:0]"))
    _print(self.check_pass("A[1]"))
    _print(self.check_pass("A[1][2]"))
    _print(self.check_pass("A[1][2][X]"))
    _print(self.check_pass("A[foo()][0][5:3]"))
    _print(self.check_pass("hoge.foo[1:0]"))
    _print(self.check_pass("hoge.foo[0][1][2][1:0]"))
    _print(self.check_fail("{1}"))
    _print(self.check_pass("{A,B}"))
    _print(self.check_pass("{{A,B},X,f}"))


if __name__=='__main__':
    run_tests()

