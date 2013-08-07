# -*- coding: utf-8 -*-
import sys
import unittest

from test_common import (
    testOf, testOfSkipped,
    print_result, run_tests, debug, grammar )

#print(dir(grammar.concatenation))

grammar.concatenation.enablePackrat()

@testOf(grammar.concatenation)
def test(self):
    #print(dir(grammar.concatenation))
    #grammar.concatenation.setBreak()
    # self.try_parse_pass("{1,2}")
    # self.try_parse_pass("{{1}}")
    self.try_parse_pass("{{{1}}}")
    self.try_parse_pass("{{{{1}}}}")
    self.try_parse_pass("{ {1,2}, {3,4,5}, {6,7, {8,9}} }")

@testOf(grammar.concatenation)
def test102(self):
    print_result(self.try_parse_pass("{1,2,3}"))
    print_result(self.try_parse_fail("{1,}"))
    print_result(self.try_parse_fail("{1,,}"))
    print_result(self.try_parse_pass("{1,1}"))
    print_result(self.try_parse_pass("{1+2,3}"))
    print_result(self.try_parse_pass("{1+2,3,X}"))
    print_result(self.try_parse_pass("{1+2,3,X,A[1]}"))
    print_result(self.try_parse_fail("{1,1,}")) 
    print_result(self.try_parse_pass("{ {1}, 1}")) 
    print_result(self.try_parse_pass("{ {1,2}, {3,4,5}, {6,7, {8,9}} }")) 
    print_result(self.try_parse_pass("{ A+B, X + 2, 3'hff }"))
 
@testOf(grammar.constant_concatenation)
def test103(self):
    print_result(self.try_parse_pass("{1,2,3}"))
    print_result(self.try_parse_pass("{1,1}"))
    print_result(self.try_parse_pass("{1+2,3}"))
    print_result(self.try_parse_pass("{1+2,3,4}"))
    print_result(self.try_parse_fail("{1,1,}")) 
    print_result(self.try_parse_pass("{ {1}, 1}")) 
    print_result(self.try_parse_pass("{ {1,2}, {3,4,5}, {6,7, {8,9}} }")) 
    print_result(self.try_parse_fail("{ A+B, X + 2, 3'hff }"))


@testOf(grammar.constant_multiple_concatenation)
def test104(self):
    # debug(grammar.constant_expression)
    # debug(grammar.constant_multiple_concatenation)
    #print_result(self.try_parse_pass("{ 0 {2,3} }"))
    pass

@testOfSkipped(grammar.module_path_concatenation)
def test105(self):
    pass


@testOfSkipped(grammar.module_path_multiple_concatenation)
def test106(self):
    pass


@testOfSkipped(grammar.multiple_concatenation)
def test107(self):
    pass


@testOf(grammar.net_concatenation)
def test108(self):
    print_result(self.try_parse_pass("{foo.bar.hoge[5].A[1] }"))
    print_result(self.try_parse_pass("{foo.bar.hoge[5].A[1][1]}"))
    print_result(self.try_parse_pass("{foo.bar.hoge[5].A[1][X]}"))
    print_result(self.try_parse_pass("{foo.bar.hoge[5].A[1][X][y]}"))
    print_result(self.try_parse_pass("{foo.bar.hoge[5].A[1][X][3:1]}"))
    print_result(self.try_parse_fail("{foo.bar.hoge[5].A[1], 4'b10 }"))
    print_result(self.try_parse_fail("{foo.bar.hoge[5].A[1][1], 8'hff }"))
    print_result(self.try_parse_fail("{foo.bar.hoge[5].A[1][X]}, 1"))
    print_result(self.try_parse_fail("{foo.bar.hoge[5].A[1][X][y]}, 10.1"))
    print_result(self.try_parse_pass("{X,Y}"))
    print_result(self.try_parse_pass("{X,Y.foo,Z[1]}"))
    print_result(self.try_parse_pass("{X[1:0],Y.foo,Z[1][2]}"))
    print_result(self.try_parse_pass("{ a, { b, c }, { d, e } }"))
    print_result(self.try_parse_pass("{ { { { { { { X } } } } } } }"))
    print_result(self.try_parse_fail("{1}"))

@testOf(grammar.net_concatenation_value)
def test109(self):
    print_result(self.try_parse_pass("foo.bar.hoge[5].A[1]"))
    print_result(self.try_parse_pass("foo.bar.hoge[5].A[1][1]"))
    print_result(self.try_parse_pass("foo.bar.hoge[5].A[1][X]"))
    print_result(self.try_parse_pass("foo.bar.hoge[5].A[1][X][y]"))
    print_result(self.try_parse_pass("foo.bar.hoge[5].A[1][X][3:1]"))
    print_result(self.try_parse_pass("A[0][func(1)][foo(2+X)]"))
    print_result(self.try_parse_fail(" 4'b10 "))
    print_result(self.try_parse_pass("{X,Y}"))
    print_result(self.try_parse_pass("{X,Y.foo,Z[1]}"))
    print_result(self.try_parse_pass("{ a, { b, c }, { d, e } }"))
    #print_result(self.try_parse_pass("10"))

@testOf(grammar.variable_concatenation)
def test110(self):
    print_result(self.try_parse_pass("{foo.bar.hoge[5].A[1] }"))
    print_result(self.try_parse_pass("{foo.bar.hoge[5].A[1][1]}"))
    print_result(self.try_parse_pass("{foo.bar.hoge[5].A[1][X]}"))
    print_result(self.try_parse_pass("{foo.bar.hoge[5].A[1][X][y]}"))
    print_result(self.try_parse_pass("{foo.bar.hoge[5].A[1][X][3:1]}"))
    print_result(self.try_parse_fail("{foo.bar.hoge[5].A[1], 4'b10 }"))
    print_result(self.try_parse_fail("{foo.bar.hoge[5].A[1][1], 8'hff }"))
    print_result(self.try_parse_fail("{foo.bar.hoge[5].A[1][X]}, 1"))
    print_result(self.try_parse_fail("{foo.bar.hoge[5].A[1][X][y]}, 10.1"))
    print_result(self.try_parse_pass("{X,Y}"))
    print_result(self.try_parse_pass("{X,Y.foo,Z[1]}"))
    print_result(self.try_parse_pass("{X[1:0],Y.foo,Z[1][2]}"))
    print_result(self.try_parse_pass("{ a, { b, c }, { d, e } }"))
    print_result(self.try_parse_pass("{ { { { { { { X } } } } } } }"))

@testOf(grammar.variable_concatenation_value)
def test111(self):
    print_result(self.try_parse_pass("foo.bar.hoge[5].A[1]"))
    print_result(self.try_parse_pass("foo.bar.hoge[5].A[1][1]"))
    print_result(self.try_parse_pass("foo.bar.hoge[5].A[1][X]"))
    print_result(self.try_parse_pass("foo.bar.hoge[5].A[1][X][y]"))
    print_result(self.try_parse_pass("foo.bar.hoge[5].A[1][X][3:1]"))
    print_result(self.try_parse_fail(" 4'b10 "))
    print_result(self.try_parse_pass("{X,Y}"))
    print_result(self.try_parse_pass("{X,Y.foo,Z[1]}"))
    print_result(self.try_parse_pass("{ a, { b, c }, { d, e } }"))


if __name__=='__main__':
    run_tests()
