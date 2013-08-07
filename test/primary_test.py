# -*- coding: utf-8 -*-
import sys
import unittest

from test_common import (
    testOf, testOfSkipped,
    print_result, run_tests, debug, grammar )

@testOf(grammar.concatenation)
def _test131(self):
    print_result(self.try_parse_fail("{1,2,}"))

@testOf(grammar.constant_primary)
def test131(self):
    print_result(self.try_parse_fail("{1,2,}"))
    print_result(self.try_parse_pass("1"))
    print_result(self.try_parse_pass("{1,2,3}"))
    print_result(self.try_parse_fail("{1,2,}"))
    print_result(self.try_parse_pass("(1)"))
    print_result(self.try_parse_pass("({1,2,3})"))
    print_result(self.try_parse_pass("func(0,1,2)"))
    print_result(self.try_parse_pass("func(0?1:2)"))
    print_result(self.try_parse_pass("{{{{1}}}}"))
    print_result(self.try_parse_fail("A"))
    
@testOfSkipped(grammar.module_path_primary)
def test132(self):
    pass

@testOf(grammar.expression)
def _test133(self):
    print_result(self.try_parse_pass("-10"))

@testOf(grammar.primary)
def test133(self):
    print_result(self.try_parse_fail("-10"))
    print_result(self.try_parse_pass("foo(1)"))
    print_result(self.try_parse_pass("$display(a,b,c)"))
    print_result(self.try_parse_pass("foo.bar.hoge[5].A[1]"))
    print_result(self.try_parse_pass("foo.bar.hoge[5].A[1][1:0]"))
    print_result(self.try_parse_pass("foo.bar.hoge[5].A[1][X]"))
    print_result(self.try_parse_pass("foo.bar.hoge[5].A[1][X][y]"))
    print_result(self.try_parse_pass("foo.bar.hoge[5].A[1][X][3:1]"))
    print_result(self.try_parse_pass("{1,2,3}"))
    print_result(self.try_parse_pass("(10)"))

@testOf(grammar.net_lvalue)
def test134(self):
    # debug(grammar.constant_expression)
    # debug(grammar.constant_range_expression)
    print_result(self.try_parse_pass("A"))
    print_result(self.try_parse_pass("A[1:0]"))
    print_result(self.try_parse_pass("A[1]"))
    print_result(self.try_parse_pass("A[1][2]"))
    print_result(self.try_parse_fail("A[1][2][X]"))
    print_result(self.try_parse_pass("A[foo()][0][5:3]"))
    print_result(self.try_parse_pass("hoge.foo[1:0]"))
    print_result(self.try_parse_pass("hoge.foo[0][1][2][1:0]"))
    print_result(self.try_parse_fail("{1}"))
    print_result(self.try_parse_pass("{A,B}"))
    print_result(self.try_parse_pass("{{A,B},X,f}"))

@testOf(grammar.variable_lvalue)
def test135(self):
    print_result(self.try_parse_pass("A"))
    print_result(self.try_parse_pass("A[1:0]"))
    print_result(self.try_parse_pass("A[1]"))
    print_result(self.try_parse_pass("A[1][2]"))
    print_result(self.try_parse_pass("A[1][2][X]"))
    print_result(self.try_parse_pass("A[foo()][0][5:3]"))
    print_result(self.try_parse_pass("hoge.foo[1:0]"))
    print_result(self.try_parse_pass("hoge.foo[0][1][2][1:0]"))
    print_result(self.try_parse_fail("{1}"))
    print_result(self.try_parse_pass("{A,B}"))
    print_result(self.try_parse_pass("{{A,B},X,f}"))


if __name__=='__main__':
    run_tests()

