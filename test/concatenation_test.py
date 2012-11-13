# -*- coding: utf-8 -*-
import sys
import unittest

from test_common import testOf, _print, run_tests, debug, grammar

#print(dir(grammar.concatenation))

grammar.concatenation.enablePackrat()

@testOf(grammar.concatenation)
def test(self):
    #print(dir(grammar.concatenation))
    #grammar.concatenation.setBreak()
    # self.check_pass("{1,2}")
    # self.check_pass("{{1}}")
    self.check_pass("{{{1}}}")
    self.check_pass("{{{{1}}}}")
    self.check_pass("{ {1,2}, {3,4,5}, {6,7, {8,9}} }")

@testOf(grammar.concatenation)
def test102(self):
    _print(self.check_pass("{1,2,3}"))
    _print(self.check_fail("{1,}"))
    _print(self.check_fail("{1,,}"))
    _print(self.check_pass("{1,1}"))
    _print(self.check_pass("{1+2,3}"))
    _print(self.check_pass("{1+2,3,X}"))
    _print(self.check_pass("{1+2,3,X,A[1]}"))
    _print(self.check_fail("{1,1,}")) 
    _print(self.check_pass("{ {1}, 1}")) 
    _print(self.check_pass("{ {1,2}, {3,4,5}, {6,7, {8,9}} }")) 
    _print(self.check_pass("{ A+B, X + 2, 3'hff }"))
 
@testOf(grammar.constant_concatenation)
def test103(self):
    _print(self.check_pass("{1,2,3}"))
    _print(self.check_pass("{1,1}"))
    _print(self.check_pass("{1+2,3}"))
    _print(self.check_pass("{1+2,3,4}"))
    _print(self.check_fail("{1,1,}")) 
    _print(self.check_pass("{ {1}, 1}")) 
    _print(self.check_pass("{ {1,2}, {3,4,5}, {6,7, {8,9}} }")) 
    _print(self.check_fail("{ A+B, X + 2, 3'hff }"))


@testOf(grammar.constant_multiple_concatenation)
def test104(self):
    # debug(grammar.constant_expression)
    # debug(grammar.constant_multiple_concatenation)
    #_print(self.check_pass("{ 0 {2,3} }"))
    pass

@testOf(grammar.module_path_concatenation)
def test105(self):
    pass


@testOf(grammar.module_path_multiple_concatenation)
def test106(self):
    pass


@testOf(grammar.multiple_concatenation)
def test107(self):
    pass


@testOf(grammar.net_concatenation)
def test108(self):
    _print(self.check_pass("{foo.bar.hoge[5].A[1] }"))
    _print(self.check_pass("{foo.bar.hoge[5].A[1][1]}"))
    _print(self.check_pass("{foo.bar.hoge[5].A[1][X]}"))
    _print(self.check_pass("{foo.bar.hoge[5].A[1][X][y]}"))
    _print(self.check_pass("{foo.bar.hoge[5].A[1][X][3:1]}"))
    _print(self.check_fail("{foo.bar.hoge[5].A[1], 4'b10 }"))
    _print(self.check_fail("{foo.bar.hoge[5].A[1][1], 8'hff }"))
    _print(self.check_fail("{foo.bar.hoge[5].A[1][X]}, 1"))
    _print(self.check_fail("{foo.bar.hoge[5].A[1][X][y]}, 10.1"))
    _print(self.check_pass("{X,Y}"))
    _print(self.check_pass("{X,Y.foo,Z[1]}"))
    _print(self.check_pass("{X[1:0],Y.foo,Z[1][2]}"))
    _print(self.check_pass("{ a, { b, c }, { d, e } }"))
    _print(self.check_pass("{ { { { { { { X } } } } } } }"))
    _print(self.check_fail("{1}"))

@testOf(grammar.net_concatenation_value)
def test109(self):
    _print(self.check_pass("foo.bar.hoge[5].A[1]"))
    _print(self.check_pass("foo.bar.hoge[5].A[1][1]"))
    _print(self.check_pass("foo.bar.hoge[5].A[1][X]"))
    _print(self.check_pass("foo.bar.hoge[5].A[1][X][y]"))
    _print(self.check_pass("foo.bar.hoge[5].A[1][X][3:1]"))
    _print(self.check_pass("A[0][func(1)][foo(2+X)]"))
    _print(self.check_fail(" 4'b10 "))
    _print(self.check_pass("{X,Y}"))
    _print(self.check_pass("{X,Y.foo,Z[1]}"))
    _print(self.check_pass("{ a, { b, c }, { d, e } }"))
    #_print(self.check_pass("10"))

@testOf(grammar.variable_concatenation)
def test110(self):
    _print(self.check_pass("{foo.bar.hoge[5].A[1] }"))
    _print(self.check_pass("{foo.bar.hoge[5].A[1][1]}"))
    _print(self.check_pass("{foo.bar.hoge[5].A[1][X]}"))
    _print(self.check_pass("{foo.bar.hoge[5].A[1][X][y]}"))
    _print(self.check_pass("{foo.bar.hoge[5].A[1][X][3:1]}"))
    _print(self.check_fail("{foo.bar.hoge[5].A[1], 4'b10 }"))
    _print(self.check_fail("{foo.bar.hoge[5].A[1][1], 8'hff }"))
    _print(self.check_fail("{foo.bar.hoge[5].A[1][X]}, 1"))
    _print(self.check_fail("{foo.bar.hoge[5].A[1][X][y]}, 10.1"))
    _print(self.check_pass("{X,Y}"))
    _print(self.check_pass("{X,Y.foo,Z[1]}"))
    _print(self.check_pass("{X[1:0],Y.foo,Z[1][2]}"))
    _print(self.check_pass("{ a, { b, c }, { d, e } }"))
    _print(self.check_pass("{ { { { { { { X } } } } } } }"))

@testOf(grammar.variable_concatenation_value)
def test111(self):
    _print(self.check_pass("foo.bar.hoge[5].A[1]"))
    _print(self.check_pass("foo.bar.hoge[5].A[1][1]"))
    _print(self.check_pass("foo.bar.hoge[5].A[1][X]"))
    _print(self.check_pass("foo.bar.hoge[5].A[1][X][y]"))
    _print(self.check_pass("foo.bar.hoge[5].A[1][X][3:1]"))
    _print(self.check_fail(" 4'b10 "))
    _print(self.check_pass("{X,Y}"))
    _print(self.check_pass("{X,Y.foo,Z[1]}"))
    _print(self.check_pass("{ a, { b, c }, { d, e } }"))


if __name__=='__main__':
    run_tests()
